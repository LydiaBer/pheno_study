#pragma once
#include <array>
#include <cstdio>
#include <functional>
#include <memory>
#include <stdexcept>
#include <string>
#include <tuple>
#include <type_traits>
#include <utility>
#include <vector>

#include <fmt/format.h>
#include <boost/callable_traits.hpp>

#include <TDirectoryFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <ROOT/RDataFrame.hxx>

namespace ct = boost::callable_traits;
template <class... Ts> class OutputTree : public ROOT::Detail::RDF::RActionImpl<OutputTree<Ts...>> {
  public:
    using Result_t = TTree;
    OutputTree(const char* name,        ///< Tree name
               TDirectoryFile* file,    ///< TDirectory or TFile to write tree into
               std::size_t num_workers, ///< Number of worker threads
               const std::tuple<const char*,
                                Ts>&... output_branches ///< Tuples of output branch names
                                                        ///< and functions to generate
                                                        ///< them. All functions must have
                                                        ///< the same argument list
                                                        ///< matching input_branches
               )
        : name(name),
          file(file),
          num_workers(num_workers),
          output_branches{std::get<0>(output_branches)...},
          functions{std::get<1>(output_branches)...},
          result_tree(nullptr),
          trees(),
          branch_data() {
        check_arg_list<0>();
    }

    OutputTree() = delete;
    OutputTree(const OutputTree&) = delete;
    OutputTree(OutputTree&& other)
        : name(std::move(other.name)),
          file(other.file),
          num_workers(other.num_workers),
          output_branches(std::move(other.output_branches)),
          functions(std::move(other.functions)),
          result_tree(std::move(other.result_tree)),
          trees(),
          branch_data() {
        other.name = "";
        other.file = nullptr;
    }

    OutputTree(const char* name, TDirectoryFile* file, std::size_t num_workers,
               const OutputTree<Ts...>& other)
        : name(name),
          file(file),
          num_workers(num_workers),
          output_branches(other.output_branches),
          functions(other.functions),
          result_tree(nullptr),
          trees(),
          branch_data() {
        ///< Use the same branch list as another OutputTree
    }

    void Initialize() {
        if (file == nullptr) {
            throw std::logic_error("OutputTrees with a nullptr `file` should only be used as "
                                   "templates for constructing other OutputTrees");
        }
        branch_data.resize(num_workers);

        // Setup trees
        for (std::size_t i = 0; i < num_workers; ++i) {
            trees.push_back(std::make_unique<TTree>());
            trees[i]->SetDirectory(nullptr);
            make_branches<0>(i);
        }
    };

    void InitTask(TTreeReader*, unsigned int) {
        // Nothing to do here
    }

    template <class... Args> void Exec(unsigned int slot, Args... args) {
        fill_branches<0>(slot, args...);
        trees[slot]->Fill();
    }

    void Finalize() {
        fmt::print("Writing TTree - {}...\n", name);
        TList temp_list;
        for (auto&& tree : trees) {
            temp_list.Add(tree.get());
        }

        file->cd();
        TTree* tree = TTree::MergeTrees(&temp_list);
        if (!tree) {
            fmt::print("ALL TREES EMPTY\n");
            return;
        }
        tree->SetName(name.c_str());
        tree->Write("", TObject::kOverwrite);
        result_tree.reset(tree);
    }

    std::shared_ptr<Result_t> GetResultPtr() { return result_tree; }
    std::string GetActionName() { return "OutputTree"; }

  private:
    static constexpr int num_branches = sizeof...(Ts);
    std::string name;
    TDirectoryFile* file; // Pointer is const, not TDirectoryFile
    const std::size_t num_workers;
    const std::array<std::string, num_branches> output_branches;
    const std::tuple<Ts...> functions;
    std::shared_ptr<Result_t> result_tree;

    std::vector<std::unique_ptr<TTree>> trees{};
    std::vector<std::tuple<typename ct::return_type_t<Ts>...>> branch_data;

    using input_branch_types = ct::args_t<decltype(std::get<0>(functions))>;
    template <int n> constexpr void check_arg_list() {
        static_assert(n < num_branches, "Called check_arg_list with n >= num_branches");
        static_assert(
              std::is_same_v<ct::args_t<decltype(std::get<n>(functions))>, input_branch_types>,
              "All functions in an OutputTree must have the same argument list");
        if constexpr (n < num_branches - 1) {
            check_arg_list<n + 1>();
        }
    }

    template <int n, class... Args> void fill_branches(unsigned int slot, Args... args) {
        static_assert(n < num_branches, "Called fill_branches with n >= num_branches");
        std::get<n>(branch_data[slot]) = std::invoke(std::get<n>(functions), args...);
        if constexpr (n < num_branches - 1) {
            fill_branches<n + 1>(slot, args...);
        }
    }

    template <int n> void make_branches(unsigned int slot) {
        // recursive creates branches in tree[slot]
        static_assert(n < num_branches, "Called make_branches with n >= num_branches");
        trees[slot]->Branch(std::get<n>(output_branches).c_str(), &std::get<n>(branch_data[slot]));
        if constexpr (n < num_branches - 1) {
            make_branches<n + 1>(slot);
        }
    }
};
