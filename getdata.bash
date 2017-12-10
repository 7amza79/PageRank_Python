#!/bin/bash


filename=$1

#get data and store it in file matrix.txt

curl  -H accept:application/json -H content-type:application/json -d '{"statements":[{"statement":"MATCH (g:node) \n WITH g \n ORDER BY g.name \n WITH COLLECT(g) AS groups \n UNWIND groups AS g1 \n UNWIND groups AS g2 \n OPTIONAL MATCH path = (g1)-[:Linked_To]->(g2) \n WITH g1, g2, CASE WHEN path is null THEN 0 \n ELSE COUNT(path) END AS overlap \n ORDER BY g1.name, g2.name \n RETURN g1.name, COLLECT(overlap) \n ORDER BY g1.name"}]}' http://localhost:7474/db/data/transaction/commit | jq -c '.results[0] | .columns,.data[].row[1] ' | sed -n '1!p' | tr -d '[]' > $filename


