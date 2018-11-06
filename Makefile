YEARS = 2013 2014 2015 2016 2017 2018 2019

URL_2013 = https://www.cityofchicago.org/content/dam/city/depts/obm/supp_info/2013%20Budget/2013BUDGETRECFINAL.pdf
URL_2014 = https://www.cityofchicago.org/content/dam/city/depts/obm/supp_info/2014%20Budget/2014RecBook.pdf
URL_2015 = https://www.cityofchicago.org/content/dam/city/depts/obm/supp_info/2015Budget/2015_Budget_REC_web.pdf
URL_2016 = https://www.cityofchicago.org/content/dam/city/depts/obm/supp_info/2016Budget/2016BudgetRecommendations.pdf
URL_2017 = https://www.cityofchicago.org/content/dam/city/depts/obm/supp_info/2017%20Budget/2017BudgetRecommendations.pdf
URL_2018 = https://www.cityofchicago.org/content/dam/city/depts/obm/supp_info/2018Budget/2018_Budget_Recommendations.pdf
URL_2019 = https://www.cityofchicago.org/content/dam/city/depts/obm/supp_info/2019Budget/2019BudgetRecommendations.pdf

PG_2013 = 43-488
PG_2014 = 44-496
PG_2015 = 45-506
PG_2016 = 55-507
PG_2017 = 46-510
PG_2018 = 45-515
PG_2019 = 50-521

GENERATED_FILES = $(foreach y, $(YEARS), output/$(y).csv)

.PHONY: all clean

.PRECIOUS: output/%.csv input/%.pdf

all: $(GENERATED_FILES)

clean:
	rm -f input/*.pdf output/*.csv

output/%.csv: input/%.pdf tabula.jar
	java -jar tabula.jar -p $(PG_$*) -c 283,366,437,507,579 $< | \
	python scripts/process_pdf.py > $@

input/%.pdf:
	wget -O $@ $(URL_$*)

tabula.jar:
	wget -O $@ https://github.com/tabulapdf/tabula-java/releases/download/v1.0.2/tabula-1.0.2-jar-with-dependencies.jar
