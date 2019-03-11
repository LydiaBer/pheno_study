#include "Cutflow.h"

#include <algorithm>
#include <string>
#include <vector>

#include <RtypesCore.h>
#include <TFile.h>
#include <TH1I.h>

ULong64_t Cutflow::get(const std::string& label) {
    auto iter = std::find(labels.begin(), labels.end(), label);
    if (iter == labels.end()) {
        return 0;
    }
    return values[iter - labels.begin()].GetValue();
}

void Cutflow::write() {
    TH1F cutflow(name.c_str(), name.c_str(), labels.size(), 0, labels.size() + 1);
    cutflow.SetDirectory(file);
    for (int i = 1; i <= labels.size(); ++i) {
        cutflow.GetXaxis()->SetBinLabel(i, labels[i - 1].c_str());
        cutflow.SetBinContent(i, values[i - 1].GetValue());
    }
    file->cd();
    cutflow.Write();
}
