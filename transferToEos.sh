#Script to take completed GN1 jobs, skim them and transfer them to /eos

mkdir replicaLists

#get file replicas on eos from GN1 jobs
while read a; do
    dsid=$(echo $a | cut -d'.' -f3)
    rucio list-file-replicas $a | grep "eos/atlas" | cut -d':' -f4 | cut -d' ' -f1 > replicaLists/files_$dsid.txt
done<GNP1DonePandaJobs_mc16e.log

#remove the extra nonsense
sed -i 's/1094\///g' replicaLists/files_*

ls replicaLists/files_* > inReplicas.txt

#skim, transfer each to eos space
while read a; do
    fileArray=$(cat $a | tr '\n' ' ')
    python calcScaleNom.py $fileArray
done<inReplicas.txt
