PG_2018 = 45-515
PG_2019 = 50-521

.PHONY: all clean

all: output/2018.csv output/2019.csv

clean:
	rm output/*.csv

output/%.csv: input/%.pdf tabula.jar
	java -jar tabula.jar -p $(PG_$*) -c 283,366,437,507,579 $< | \
	python scripts/process_pdf.py > $@

tabula.jar:
	wget -O $@ https://github.com/tabulapdf/tabula-java/releases/download/v1.0.2/tabula-1.0.2-jar-with-dependencies.jar
