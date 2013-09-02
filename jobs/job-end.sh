
# EKSPORT WYNIKOW
printf "\n Copy output files\n"
sha1sum $OUTPUT > sha1_output.sum.$JOB_ID
cp -vrn $OUTPUT sha1_output.sum.$JOB_ID $SRC_DIR/

cd $SRC_DIR

printf "\n Verify copied files\n"
sha1sum -c sha1_output.sum.$JOB_ID

if [ $? -ne 0 ]
then
  printf "\n\n Corruption while copying output data files\n "
  echo " Try again to copy files from $WORKDIR at $HOSTNAME"
else
  rm -r $WORKDIR
fi

mv *_*_*_*_*.xml.bz2 results/
mv std.{out,err}.* mchudak-dynamo.{o,e}* log/
rm sha1_*.sum.$JOB_ID

exit 0
