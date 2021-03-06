#$ -S /bin/bash
#$ -cwd
#$ -q standard              # docelowa kolejka dla zadania
#$ -N mchudak-dynamo        # nazwa zadania w systemie kolejkowym

# W SKRYPCIE NALEZY OKRESLIC
#   * nazwe programu (PROG_01)
#   * liste plikow potrzebnych do uruchomienia programu (INPUT)
#   * liste plikow wynikowych (OUTPUT)
#   * opcjonalnie zmiane kolejki  powy�ej '#$ -q' dostepne opcje: standard,fem
#   * nazwa zadania okre�lona w `#$ -N` bedzie widoczna w systemie kolejkowym
#   * dodatkowe czynno�ci przed i po uruchomieniu programu (jak rozpakowywanie
#      pakowanie plikow) nalezy umiescic odpowiednio w sekcji PREPROCESSING
#      oraz POSPROCESSING
# Skrypt nale�y zapisa� w katalogu z zadaniem do obliczenia i uruchomi�
# poleceniem
#               qsub <nazwa_pliku_ze_skryptem>
# Skrypt musi byc wykonywalny
#               chmod +x <nazwa_pliku_ze_skryptem>

date
echo " Job running on: $HOSTNAME"

export PATH=/opt/DynamO/bin:$PATH
export LD_LIBRARY_PATH=/opt/DynamO/lib:$LD_LIBRARY_PATH

SRC_DIR=`pwd`
TMP_PATH="/scratch"
NODE_WORKDIR_NAME="`printf "%s_ID-%08d_R%08d" $USER $JOB_ID $RANDOM`"
WORKDIR="$TMP_PATH/$NODE_WORKDIR_NAME"
TMPDIRS="configs results log"

#input
PROG_01="convergence.py"
INPUT="my_helper_functions_bare.py"

#output
OUTPUT="results/* log/*"

# Tworzenie katalogu tymczasowego na wezle
# if [ ! -d $TMP_PATH/$NODE_WORKDIR_NAME ]
if [ ! -d $WORKDIR ]
then
#   WORKDIR=`mktemp --tmpdir=$TMP_PATH -td ${NODE_WORKDIR_NAME}.XXXXXX`
    mkdir $WORKDIR
fi

# kopiowanie programu(-ow) i danych wejsciowych
printf "\n Copy input files\n"
sha1sum $PROG_01 $INPUT > sha1_input.sum.$JOB_ID
cp -v $PROG_01 $INPUT sha1_input.sum.$JOB_ID $WORKDIR/
rm sha1_input.sum.$JOB_ID

cd $WORKDIR
if [ $? -ne 0 ]
then
  echo " Can't change to WORKDIR"
  exit 1
else
  echo " Working in `pwd`"
fi

printf "\n Verify copied files\n"
sha1sum -c sha1_input.sum.$JOB_ID

if [ $? -ne 0 ]
then
  echo " Corruption while cupying input data files"
  exit 1
fi

# URUCHAMIANIE PROGRAMU

mkdir $TMPDIRS
echo "Job $JOB_ID is executed on $HOSTNAME, command: ./convergence.py 0.7 1>convergence.out 2>convergence.err"
./convergence.py 0.7 1>convergence.out 2>convergence.err

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

rm sha1_output.sum.$JOB_ID 
mv *_*_*_*_*.xml.bz2 results/
mv std.{out,err}.* mchudak-dynamo.{o,e}* log/

exit 0
