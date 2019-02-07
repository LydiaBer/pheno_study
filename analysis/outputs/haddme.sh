### Signal ###

hadd resolved_loop_hh.root resolved_loop_hh_sample*.root 
hadd intermediate_loop_hh.root intermediate_loop_hh_sample*.root 
hadd boosted_loop_hh.root boosted_loop_hh_sample*.root

### Bkg ###

# No pT filter
# QCD 
hadd resolved_noGenFilt_2b2j.root resolved_noGenFilt_2b2j_sample*.root 
hadd intermediate_noGenFilt_2b2j.root intermediate_noGenFilt_2b2j_sample*.root 
hadd boosted_noGenFilt_2b2j.root boosted_noGenFilt_2b2j_sample*.root 

hadd resolved_noGenFilt_4b.root resolved_noGenFilt_4b_sample*.root 
hadd intermediate_noGenFilt_4b.root intermediate_noGenFilt_4b_sample*.root 
hadd boosted_noGenFilt_4b.root boosted_noGenFilt_4b_sample*.root 

hadd resolved_noGenFilt_4j.root resolved_noGenFilt_4j_sample*.root 
hadd intermediate_noGenFilt_4j.root intermediate_noGenFilt_4j_sample*.root 
hadd boosted_noGenFilt_4j.root boosted_noGenFilt_4j_sample*.root 

hadd resolved_noGenFilt_ttbar.root resolved_noGenFilt_ttbar_sample*.root 
hadd intermediate_noGenFilt_ttbar.root intermediate_noGenFilt_ttbar_sample*.root 
hadd boosted_noGenFilt_ttbar.root boosted_noGenFilt_ttbar_sample*.root 

# H
hadd resolved_noGenFilt_wh.root resolved_noGenFilt_wh_sample*.root 
hadd intermediate_noGenFilt_wh.root intermediate_noGenFilt_wh_sample*.root 
hadd boosted_noGenFilt_wh.root boosted_noGenFilt_wh_sample*.root 

hadd resolved_noGenFilt_zh.root resolved_noGenFilt_zh_sample*.root 
hadd intermediate_noGenFilt_zh.root intermediate_noGenFilt_zh_sample*.root 
hadd boosted_noGenFilt_zh.root boosted_noGenFilt_zh_sample*.root 

hadd resolved_noGenFilt_tth.root resolved_noGenFilt_tth_sample*.root 
hadd intermediate_noGenFilt_tth.root intermediate_noGenFilt_tth_sample*.root 
hadd boosted_noGenFilt_tth.root boosted_noGenFilt_tth_sample*.root 

# pT filter
# QCD 
hadd resolved_xpt200_2b2j.root resolved_xpt200_2b2j_sample*.root 
hadd intermediate_xpt200_2b2j.root intermediate_xpt200_2b2j_sample*.root 
hadd boosted_xpt200_2b2j.root boosted_xpt200_2b2j_sample*.root 

hadd resolved_xpt200_4b.root resolved_xpt200_4b_sample*.root 
hadd intermediate_xpt200_4b.root intermediate_xpt200_4b_sample*.root 
hadd boosted_xpt200_4b.root boosted_xpt200_4b_sample*.root 

hadd resolved_xpt200_4j.root resolved_xpt200_4j_sample*.root 
hadd intermediate_xpt200_4j.root intermediate_xpt200_4j_sample*.root 
hadd boosted_xpt200_4j.root boosted_xpt200_4j_sample*.root 

mkdir separate
mv *sample*.root separate  
