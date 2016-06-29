ROOTCFLAGS    = $(shell root-config --cflags)
ROOTGLIBS     = $(shell root-config --glibs)

CXX            = g++
CXXFLAGS       = -fPIC -Wall -O3 -g
CXXFLAGS       += $(filter-out -stdlib=libc++ -pthread , $(ROOTCFLAGS))
GLIBS          = $(filter-out -stdlib=libc++ -pthread , $(ROOTGLIBS))

INCLUDEDIR       = ./include/
SRCDIR           = ./src/
CXX	         += -I$(INCLUDEDIR) -I.
OUTOBJ	         = ./obj/

CC_FILES := $(wildcard src/*.cc)
HH_FILES := $(wildcard include/*.hh)
OBJ_FILES := $(addprefix $(OUTOBJ),$(notdir $(CC_FILES:.cc=.o)))

all: dat2root Fit_xADC Calibrate_xADC Fit_PDO Calibrate_PDO

dat2root:  $(SRCDIR)dat2root.C $(OBJ_FILES) $(HH_FILES)
	$(CXX) $(CXXFLAGS) -o dat2root $(GLIBS) $ $<
	touch dat2root	

Fit_xADC:  $(SRCDIR)Fit_xADC.C $(OBJ_FILES) $(HH_FILES)
	$(CXX) $(CXXFLAGS) -o Fit_xADC $(GLIBS) $ $<
	touch Fit_xADC

Calibrate_xADC:  $(SRCDIR)Calibrate_xADC.C $(OBJ_FILES) $(HH_FILES)
	$(CXX) $(CXXFLAGS) -o Calibrate_xADC $(GLIBS) $ $<
	touch Calibrate_xADC

Fit_PDO:  $(SRCDIR)Fit_PDO.C $(OBJ_FILES) $(HH_FILES)
	$(CXX) $(CXXFLAGS) -o Fit_PDO $(GLIBS) $ $<
	touch Fit_PDO

Calibrate_PDO:  $(SRCDIR)Calibrate_PDO.C $(OBJ_FILES) $(HH_FILES)
	$(CXX) $(CXXFLAGS) -o Calibrate_PDO $(GLIBS) $ $<
	touch Calibrate_PDO

$(OUTOBJ)%.o: src/%.cc include/%.hh
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OUTOBJ)*.o
	rm -rf *.dSYM
	rm -f dat2root
	rm -f Fit_xADC
	rm -f Calibrate_xADC
	rm -f Fit_PDO
	rm -f Calibrate_PDO
