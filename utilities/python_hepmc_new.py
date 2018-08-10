##Python script to Split HEPMC files ONCE and FOR ALL
#we split the hepmc file in 100 small files
numb_events=100000
with open("/data/atlas/atlasdata2/DiHiggsSharedSamples/arxiv-v1/SHERPA_QCD_4b.hepmc") as infile:
	events = 0
	print "Imported File"
	for line in infile:
		if (len(line.strip())<1):
			continue
		else:	
			if events == 0 :
				final= open("4bar_split0.hepmc","w+")
				final.write("HepMC::Version 2.06.08\n")
        			final.write("HepMC::IO_GenEvent-START_EVENT_LISTING\n")
    			if line.startswith("E") and events== 0 :
				final.write(line)
			if line.startswith("HepMC::Version 2.06.09"):
				continue
   			if line.startswith("HepMC::IO_GenEvent-START_EVENT_LISTING"):
				continue
    			if line.startswith("E"):
				events+=1
    			if events% numb_events==0 and events !=0 and line.startswith("E"): 
				final.write("HepMC::IO_GenEvent-END_EVENT_LISTING")
				final.close()
				file_count = events/numb_events
        			final= open("4bar_split%d.hepmc" % file_count,"w+")
				print "Writing to", final.name
				final.write("HepMC::Version 2.06.08\n")
        			final.write("HepMC::IO_GenEvent-START_EVENT_LISTING\n")
#print "Writing to", final.name
    			final.write(line)	
    			if line.startswith("H"):
				final.close()
        			break

infile.close()
