import os
import re
import shutil

def createMain(f):
	#license
	f.write(
		"/**\n"
		"\n"
		"@copyright \n"
		"<pre>\n"
		"\n"
		"\n"
		"\tCopyright (c) 2014 Institute for Electronic Design Automation, TU Munich\n"
		"\n"
		"\tThe above copyright notice and this permission notice shall be included in\n"
		"\tall copies or substantial portions of the Software.\n"
		"\n"
		"\tTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
		"\tIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
		"\tFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
		"\tAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
		"\tLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
		"\tOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n"
		"\tTHE SOFTWARE.\n"
		"\n"
		"\n"
		"</pre>\n"
		"@author Marc Greim <marc.greim@mytum.de>\n"
		"\n"
		"@date July 29, 2014\n"
		"\n"
		"@version 0.1\n"
		"\n"
		"*/\n"
		"/**\n"
		"\t@file\n"
		"\t\n"
		"\t@brief \n"
		"\n"
		"\t@detail \n"
		"\t\t\n"
		"\t\t\n"
		"\t\t\n"
		"\n"
		"*/\n"
		)
	#headers
	f.write("#include <map>\n"
		"#include <iostream>\n"
		"#include <memory>\n"
		"#include <cstring>\n"
		"#include <sstream>\n"
		"\n"
		"#include \"etiss/ETISS.h\"\n"
		"#include \"etiss/DebugSystem.h\"\n"
		"\n"
		)
	#main
	f.write(
		"int main( int argc, const char* argv[] ) {\n"
		"\n"
		"\tstd::vector<std::string> vargs;\n"
		"\tfor (int i = 0;i<argc;i++){\n"
		"\t\tvargs.push_back(argv[i]);\n"
		"\t}\n"
		"\t\n"
		"\tvargs.push_back(\"-oetiss_path\");\n"
		"\tvargs.push_back(\""+re.escape(etisspath)+"\");\n"
		"\t\n"
		"\tetiss::initialize(vargs);\n"
		"\t{\n"
		"\t\tetiss::DebugSystem dsys;\n"
		"\t\n"
		"\t\t// load some image\n"
		"\t\tdsys.load(0,\"./code.bin\");\n"
		"\t\n"
		"\t\t// general option map\n"
		"\t\tstd::map<std::string,std::string> options;\n"
		"\t\n"
		"\t\toptions.clear();\n"
		"\t\t//options[\"norangeexception\"] = \"true\"; // disable range exceptions\n"
		"\t\t//options[\"returnjump\"] = \"true\"; // block dosn't end after jump\n"
		"\t\tstd::shared_ptr<etiss::CPUCore> cpu = etiss::CPUCore::create(\"or1k\",\"core0\",options);\n"
		"\t\n"
		"\t\n"
		"\t\n"
		"\t\tif (cpu.get() == 0){\n"
		"\t\t\tetiss::log(etiss::FATALERROR,\"failed to create cpu core\");\n"
		"\t\t\treturn -1;\n"
		"\t\t}\n"
		"\t\n"
		"\t\tcpu->set(etiss::getJIT(\"LLVMJIT\"));\n"
		"\t\n"
		"\t\n"
		"\t\t// reset with given initial address\n"
		"\t\t//etiss::uint64 sa = 0;\n"
		"\t\t//cpu->reset(&sa);\n"
		"\n"
		"\t\t\n"
		"\t\toptions.clear();\n"
		"\t\t//cpu->addPlugin(etiss::getPlugin(\"PrintInstruction\",options));\t\n"
		"\n"
		"\t\toptions.clear();\n"
		"\t\t//cpu->addPlugin(etiss::getPlugin(\"gdbserver\",options));\n"
		"\t\t\n"
		"\n"
		"\t\toptions.clear();\t\t\n"
		"\t\t//options[\"-rR5\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR6\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR7\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR8\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR10\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR14\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR15\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR16\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR17\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR18\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR19\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR20\"] = \"./fail_set_00000\";\n"
		"\t\t\n"
		"\t\t//cpu->addPlugin(etiss::getPlugin(\"BlockAccurateHandler\",options));\n"
		"\n"
		"\t\tetiss_int32 exception = cpu->execute(dsys);\n"
		"\t\n"
		"\t\tif (exception != 0)\n"
		"\t\t\tstd::cout << \"CPU exited with exception: 0x\" <<std::hex << exception<<std::dec << std::endl;\n"
		"\t\n"
		"\t}\n"
		"\t\n"
		"\tetiss::shutdown();\n"
		"\n"
		"return 0;\n"
		"}"
		)
		
def createSystemCMain(f):
	f.write("/**\n"
		"\n"
		"@copyright \n"
		"<pre>\n"
		"\n"
		"\n"
		"\tCopyright (c) 2014 Institute for Electronic Design Automation, TU Munich\n"
		"\n"
		"\tThe above copyright notice and this permission notice shall be included in\n"
		"\tall copies or substantial portions of the Software.\n"
		"\n"
		"\tTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
		"\tIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
		"\tFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
		"\tAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
		"\tLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
		"\tOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n"
		"\tTHE SOFTWARE.\n"
		"\n"
		"\n"
		"</pre>\n"
		"@author Marc Greim <marc.greim@mytum.de>\n"
		"\n"
		"@date July 29, 2014\n"
		"\n"
		"@version 0.1\n"
		"\n"
		"*/\n"
		"/**\n"
		"\t@file\n"
		"\t\n"
		"\t@brief \n"
		"\n"
		"\t@detail \n"
		"\t\t\n"
		"\t\t\n"
		"\t\t\n"
		"\n"
		"*/\n"
		"\n"
		"#include <map>\n"
		"#include <iostream>\n"
		"#include <memory>\n"
		"#include <cstring>\n"
		"#include <sstream>\n"
		"\n"
		"#include \"SystemCBridge.h\" // SystemC <-> ETISS\n"
		"#include \"SimpleMemory.h\" // Systemc -> memory\n"
		"#include \"etiss/ETISS.h\"\n"
		"\n"
		"\n"
		"\n"
		"class DummyInterruptModule : public sc_core::sc_module {\n"
		"public:\n"
		"\tSC_HAS_PROCESS(DummyInterruptModule);\n"
		"\tDummyInterruptModule(sc_core::sc_module_name name) : sc_core::sc_module(name){\n"
		"\t\tirq_out_2.bind(irq_sig_2);\n"
		"\t\treset_out.bind(reset_sig);\n"
		"\t\tSC_THREAD(thread);\n"
		"\t}\n"
		"\tsc_out<bool> irq_out_2;\n"
		"\tsc_signal<bool> irq_sig_2;\n"
		"\tsc_out<bool> reset_out;\n"
		"\tsc_signal<bool> reset_sig;\n"
		"private:\n"
		"\tvoid thread(){\n"
		"\t//generate an interrupt\n"
		"\t/*\n"
		"\t\twait(1,SC_NS);\n"
		"\t\tirq_out_2->write(false);\n"
		"\t\twait(11830,SC_NS);\n"
		"\t\tirq_out_2->write(true);\n"
		"\t\twait(100000,SC_NS);\n"
		"\t\tirq_out_2->write(false);\n"
		"\t*/\n"
		"\t//generate a reset\n"
		"\t/*\n"
		"\t\treset_out->write(false);\n"
		"\t\twait(23000,SC_NS);\n"
		"\t\treset_out->write(true);\n"
		"\t\twait(24000,SC_NS);\n"
		"\t\treset_out->write(false);\t\n"
		"\t*/\n"
		"\t}\n"
		"};\n"
		"\n"
		"\n"
		"int  sc_main(int argc, char *argv[]){\n"
		"\n"
		"\tstd::vector<std::string> vargs;\n"
		"\tfor (int i = 0;i<argc;i++){\n"
		"\t\tvargs.push_back(argv[i]);\n"
		"\t}\n"
		"\t\n"
		"\tvargs.push_back(\"-oetiss_path\");\n"
		"\tvargs.push_back(\""+re.escape(etisspath)+"\");\n"
		"\t\n"
		"\tetiss::initialize(vargs);\n"
		"\t{\n"
		"\t\n"
		"\t\t// general option map\n"
		"\t\tstd::map<std::string,std::string> options;\n"
		"\t\n"
		"\t\toptions.clear();\n"
		"\t\t//options[\"norangeexception\"] = \"true\"; // disable range exceptions\n"
		"\t\t//options[\"returnjump\"] = \"true\"; // block dosn't end after jump\n"
		"\t\tstd::shared_ptr<etiss::CPUCore> cpu = etiss::CPUCore::create(\"or1k\",\"core0\",options);\n"
		"\t\n"
		"\t\tif (cpu.get() == 0){\n"
		"\t\t\tetiss::log(etiss::FATALERROR,\"failed to create cpu core\");\n"
		"\t\t\treturn -1;\n"
		"\t\t}\n"
		"\t\n"
		"\t\tcpu->set(etiss::getJIT(\"LLVMJIT\"));\n"
		"\t\n"
		"\t\n"
		"\t\t// reset with given initial address\n"
		"\t\t//etiss::uint64 sa = 0;\n"
		"\t\t//cpu->reset(&sa);\n"
		"\n"
		"\t\t\n"
		"\t\toptions.clear();\n"
		"\t\t//cpu->addPlugin(etiss::getPlugin(\"PrintInstruction\",options));\t\n"
		"\n"
		"\t\toptions.clear();\n"
		"\t\t//cpu->addPlugin(etiss::getPlugin(\"gdbserver\",options));\n"
		"\t\t\n"
		"\n"
		"\t\toptions.clear();\t\t\n"
		"\t\t//options[\"-rR5\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR6\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR7\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR8\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR10\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR14\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR15\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR16\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR17\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR18\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR19\"] = \"./fail_set_00000\";\n"
		"\t\t//options[\"-rR20\"] = \"./fail_set_00000\";\n"
		"\t\t\n"
		"\t\t//cpu->addPlugin(etiss::getPlugin(\"BlockAccurateHandler\",options));\n"
		"\n"
		"\t\t// create systemc interface\n"
		"\t\tSystemCBridge cpubridge(\"ETISS\",32,cpu);\n"
		"\n"
		"\t\t// create systemc memory backend\n"
		"\t\tSimpleMemory sm(\"Memory\");\n"
		"\t\t\n"
		"\t\t// connect system to memory\n"
		"\t\tcpubridge.d_bus.bind(sm.tsktForCPU_d);\n"
		"\t\tcpubridge.i_bus.bind(sm.tsktForCPU_i);\n"
		"\t\t\n"
		"\t\t// load image to memory\n"
		"\t\tsm.load(0,\"./code.bin\");\n"
		"\t\t\n"
		"\t\tDummyInterruptModule dim(\"dim\");\n"
		"\t\tsc_in<bool> * irq_in_2 = cpubridge.allocateIRQ(2);\n"
		"\t\tirq_in_2->bind(dim.irq_sig_2);\n"
		"\t\tsc_in<bool> * reset_in = cpubridge.allocateReset();\n"
		"\t\treset_in->bind(dim.reset_sig);\n"
		"\n"
		"\t\tsc_start(3000, SC_MS);\n"
		"\t\n"
		"\t}\n"
		"\t\n"
		"\tetiss::shutdown();\n"
		"\n"
		"return 0;\n}"
		)

def createSystemCMakefile(f,etisspath,syschome,target_arch,tlmhome):
	f.write("#make directories if not present\n"
		"$(shell mkdir -p ./build)\n"
		"\n"
		"CC = gcc\n"
		"CFLAGS = -std=c++0x -Wall -Wno-deprecated -Wno-unused -Wno-parentheses -fpermissive -fPIC \n"
		"\n"
		"ifeq ($(DEBUG),0)\n"
		"\tDBGPARAM =\n"
		"\tOPTLEVEL?=-Ofast\n"
		"else\n"
		"\tDBGPARAM =-g\n"
		"\tOPTLEVEL?=\n"
		"endif\n"
		"\n"
		"CFLAGS+= $(OPTLEVEL) $(DBGPARAM) \n"
		"\n"
		"\n"
		"#######################################\n"
		"# adapt these paths if needed\n"
		"SYSTEMC_HOME="+syschome+"\n"
		"TLM_HOME="+tlmhome+"\n"
		"SYSTEMC_LIBS= -lstdc++ -lm  -lpthread \n"
		"TARGET_ARCH="+target_arch+"\n"
		"ETISS_HOME="+etisspath+"\n"
		"######################################\n"
		"\n"
		"SYSTEMC_FLAGS=${CFLAGS} -DSC_INCLUDE_DYNAMIC_PROCESSES -I${SYSTEMC_HOME}/include -L${SYSTEMC_HOME}/lib-${TARGET_ARCH} -I${TLM_HOME}/include/tlm -I$(ETISS_HOME)/include -I$(ETISS_HOME)/include_c \n"
		"\n"
		"\n"
		"TARGETFILES=$(wildcard *.cpp)\n"
		"TARGETFILESCLEAN=$(filter-out main.cpp,$(TARGETFILES))\n"
		"OBJFILES:=$(TARGETFILESCLEAN:%.cpp=build/%.o)\n"
		"\n"
		"\n"
		"\n"
		"all: main\n"
		"\n"
		"build/%.o: %.cpp\n"
		"\t$(CC) -c $(SYSTEMC_FLAGS)  -MMD -o $@ $<\n"
		"\n"
		"-include build/*.d\n"
		"\n"
		"$(ETISS_HOME)/libETISS.so:\n"
		"\tcd $(ETISS_HOME) && make libETISS.so\n"
		"\n"
		"main: $(OBJFILES) main.cpp $(ETISS_HOME)/libETISS.so\n"
		"\tg++ $(SYSTEMC_FLAGS) main.cpp -L$(ETISS_HOME) -o main  $(OBJFILES) ${SYSTEMC_HOME}/lib-${TARGET_ARCH}/libsystemc.a -ldl -lETISS ${SYSTEMC_LIBS}\n"
		"\n"
		".PHONY: run\n"
		"run:  \tmain\n"
		"\tLD_LIBRARY_PATH=$(ETISS_HOME):${SYSTEMC_HOME}/lib-${TARGET_ARCH}:$LD_LIBRARY_PATH ./main\n"
		"\n"
		".PHONY: gdb\n"
		"gdb:\tmain\n"
		"\tLD_LIBRARY_PATH=$(ETISS_HOME):${SYSTEMC_HOME}/lib-${TARGET_ARCH}:$LD_LIBRARY_PATH gdb --args ./main\n"
		"\n"
		"-PHONY: clean\n"
		"clean:\n"
		"\trm -R -f ./build/*\n"
		"\trm -f main"
		)
		
def createMainMakefile(f,etisspath):
	f.write("#make directories if not present\n"
		"$(shell mkdir -p ./build)\n"
		"\n"
		"CC = gcc\n"
		"CFLAGS = -std=c++0x -Wall -Wno-deprecated -Wno-unused -Wno-parentheses -fpermissive -fPIC \n"
		"\n"
		"ifeq ($(DEBUG),0)\n"
		"\tDBGPARAM =\n"
		"\tOPTLEVEL?=-Ofast\n"
		"else\n"
		"\tDBGPARAM =-g\n"
		"\tOPTLEVEL?=\n"
		"endif\n"
		"\n"
		"CFLAGS+= $(OPTLEVEL) $(DBGPARAM) \n"
		"\n"
		"\n"
		"#######################################\n"
		"# adapt these paths if needed\n"
		"ETISS_HOME="+etisspath+"\n"
		"######################################\n"
		"\n"
		"CFLAGS+= -I$(ETISS_HOME)/include -I$(ETISS_HOME)/include_c \n"
		"\n"
		"\n"
		"TARGETFILES=$(wildcard *.cpp)\n"
		"TARGETFILESCLEAN=$(filter-out main.cpp,$(TARGETFILES))\n"
		"OBJFILES:=$(TARGETFILESCLEAN:%.cpp=build/%.o)\n"
		"\n"
		"\n"
		"\n"
		"all: main\n"
		"\n"
		"build/%.o: %.cpp\n"
		"\t$(CC) -c $(CFLAGS)  -MMD -o $@ $<\n"
		"\n"
		"-include build/*.d\n"
		"\n"
		"$(ETISS_HOME)/libETISS.so:\n"
		"\tcd $(ETISS_HOME) && make libETISS.so\n"
		"\n"
		"main: $(OBJFILES) main.cpp $(ETISS_HOME)/libETISS.so\n"
		"\tg++ $(CFLAGS) main.cpp -L$(ETISS_HOME) -o main  $(OBJFILES) -ldl -lETISS\n"
		"\n"
		".PHONY: run\n"
		"run:  \tmain\n"
		"\tLD_LIBRARY_PATH=$(ETISS_HOME):${SYSTEMC_HOME}/lib-${TARGET_ARCH}:$LD_LIBRARY_PATH ./main\n"
		"\n"
		".PHONY: gdb\n"
		"gdb:\tmain\n"
		"\tLD_LIBRARY_PATH=$(ETISS_HOME):${SYSTEMC_HOME}/lib-${TARGET_ARCH}:$LD_LIBRARY_PATH gdb --args ./main\n"
		"\n"
		"-PHONY: clean\n"
		"clean:\n"
		"\trm -R -f ./build/*\n"
		"\trm -f main"
		)

def createProject(etisspath,path,project,sysc,syschome,target_arch,tlmhome):
    	if not os.path.exists(path):
		os.makedirs(path)
	with open(os.path.join(path,'main.cpp'),'w') as f:
		if sysc:
			createSystemCMain(f)
		else:	
			createMain(f)
	with open(os.path.join(path,'Makefile'),'w') as f:
		if sysc:
			createSystemCMakefile(f,etisspath,syschome,target_arch,tlmhome)
		else:	
			createMainMakefile(f,etisspath)
	if sysc:
		spath = os.path.join(etisspath,"systemc")
		shutil.copyfile(os.path.join(spath,"SimpleMemory.h"), os.path.join(path,"SimpleMemory.h"))
		shutil.copyfile(os.path.join(spath,"SimpleMemory.cpp"), os.path.join(path,"SimpleMemory.cpp"))
		shutil.copyfile(os.path.join(spath,"SystemCBridge.h"), os.path.join(path,"SystemCBridge.h"))
		shutil.copyfile(os.path.join(spath,"SystemCBridge.cpp"), os.path.join(path,"SystemCBridge.cpp"))
		shutil.copyfile(os.path.join(spath,"SystemCInterface.h"), os.path.join(path,"SystemCInterface.h"))
		shutil.copyfile(os.path.join(spath,"SystemCInterface.cpp"), os.path.join(path,"SystemCInterface.cpp"))
		shutil.copyfile(os.path.join(spath,"ResourceCheckout.h"), os.path.join(path,"ResourceCheckout.h"))
	
	shutil.copyfile(os.path.join(os.path.join(etisspath,"SW"),"code.bin"), os.path.join(path,"code.bin"))
	
	


import sys
args = sys.argv


etisspath = os.path.dirname(os.path.realpath(__file__))
tmp = raw_input("Set path of ETISS ["+etisspath+"]: ")
etisspath = tmp or etisspath
project = raw_input("Enter project name: ")

if os.path.dirname(os.path.realpath(__file__)) != os.getcwd():
	path = os.path.join(os.getcwd(),project)
else:
	path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),"projects"),project)
	
tmp = raw_input("Select project path ["+path+"]: ")
path = tmp or path

sysc = bool(raw_input("Is this a SystemC project?: "))


syschome = "/usr/local/research/projects/SystemDesign/tools/systemc/systemc-2.3.0"
if sysc:
	tmp = raw_input("SystemC home folder["+syschome+"]: ")
	syschome = tmp or syschome
target_arch = "linux64"
if sysc:
	tmp = raw_input("SystemC target architecture ["+target_arch+"]: ")
	target_arch = tmp or target_arch
tlmhome = "/usr/local/research/projects/SystemDesign/tools/systemc/TLM-2009-07-15"
if sysc:
	tmp = raw_input("TLM home folder["+tlmhome+"]: ")
	tlmhome = tmp or tlmhome


	
createProject(etisspath,path,project,sysc,syschome,target_arch,tlmhome)




