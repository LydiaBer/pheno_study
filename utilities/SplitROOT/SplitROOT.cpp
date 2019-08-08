// Short program to split a ROOT ntuple into 25% chunks
// Also splits based on number of large R jets
//
#include <array>
#include <string>
#include <string_view>

#include <fmt/format.h>

#include <TFile.h>
#include <TTree.h>

using namespace std::literals;

bool has_root_ext(std::string_view file) {
    auto dot = file.rfind('.');
    if (dot == std::string_view::npos || dot >= file.size() - 1) {
        return false;
    }

    if (file.substr(dot + 1, std::string_view::npos) == "root"sv) {
        return true;
    }
    else {
        return false;
    }
}

int main(int argc, char* argv[]) {
    std::array regions{"resolved"s, "intermediate"s, "boosted"s};

    for (std::size_t i = 1; i < argc; ++i) {
        // Start at 1 to skip binary name
        const char* filename = argv[i];
        if (has_root_ext(filename)) {
            // prefix is portion of filename between last / and last .
            auto filename_v = std::string_view(filename);
            std::string_view prefix = filename_v.substr(filename_v.rfind('/') + 1,
                                                        filename_v.rfind('.'));

            TFile* input = TFile::Open(filename);
            TTree* input_tree = nullptr;
            input->GetObject("preselection", input_tree);
            if (!input_tree) {
                fmt::print(stderr,
                           "File {} does not contain a preselection TTree\n",
                           filename);
                continue;
            }

            fmt::print("Processing file {}\n", filename);
            for (std::size_t n_largeR_jets = 0; n_largeR_jets < 3;
                 ++n_largeR_jets) {
                std::string selection =
                      fmt::format("n_large_jets=={}", n_largeR_jets);
                if (n_largeR_jets == 2) {
                    selection = "n_large_jets>=2";
                }

                fmt::print("\t{}: ", regions[n_largeR_jets]);
                std::fflush(stdout);

                // Looks like we *need* to create this TTree in a scratch TFile
                auto scratch_file =
                      TFile("/tmp/scratch_copy_123.root", "RECREATE");
                scratch_file.cd();
                TTree* selected = input_tree->CopyTree(selection.c_str());

                const int n_entries = selected->GetEntries();
                const int step = n_entries % 4
                                       ? n_entries / 4 + 1
                                       : n_entries / 4; // Make splits as close
                                                        // to equal as possible

                // start is first entry, j is split index
                // Comma operator lets us increment both together
                for (int start = 0, j = 0; start < n_entries;
                     start += step, ++j) {
                    std::string output_filename = fmt::format(
                          "{}.{}_{}.root", prefix, regions[n_largeR_jets], j);
                    fmt::print("{} ", j); // Print index
                    std::fflush(stdout);

                    TFile* output = TFile::Open(output_filename.c_str(), "RECREATE");
                    output->cd();
                    TTree* chunk = selected->CopyTree("", "", step, start);
                    chunk->SetDirectory(output);
                    chunk->Write();
                    output->Close();
                }

                scratch_file.cd();
                std::puts(""); // Print a newline
            }
        }
    }

    return 0;
}
