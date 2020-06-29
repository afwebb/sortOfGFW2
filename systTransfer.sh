#Script to take completed GN1 jobs, skim them and transfer them to /eos

mkdir replicaLists
runYear=sys

#get file replicas on eos from GN1 jobs
while read a; do
    #dsid=$(echo $a | cut -d'.' -f3)
    dsid=$(echo $a | cut -d'.' -f7 | cut -d'_' -f1)
    #dsid=$(echo $a | cut -d'.' -f6 | cut -d'_' -f1)
    echo $dsid
    rucio list-file-replicas $a | grep "eos/atlas" | cut -d':' -f4 | cut -d' ' -f1 > replicaLists/files_${runYear}_$dsid.txt
done<v3_$runYear.txt

#remove the extra nonsense
sed -i 's/1094\///g' replicaLists/files_${runYear}_*

ls replicaLists/files_${runYear}_* > inReplicas_${runYear}.txt

sysRun(){
    while read s; do
	python calcScaleNom.py $1 $2 $s
    done<treeList.txt
}

#skim, transfer each to eos space
while read a; do
    sysRun $a $runYear &
done<inReplicas_$runYear.txt
