RISCV=riscv-none-elf-
RISCV_GCC_OPTS=-T./custom/test.ld -static -mcmodel=medany \
	       -fvisibility=hidden -nostdlib -nostartfiles -g \
	       ./custom/crt.S -I ./custom -march=rv32ima_zicsr -mabi=ilp32 
    
SOURCES := $(wildcard asms/*.s)
BINS    := $(patsubst asms/%.s,bins/%.r5o,$(SOURCES))
DUMPS   := $(patsubst bins/%.r5o,dumps/%.r5o.dump,$(BINS))
RUNS    := $(patsubst asms/%.s,runs/%,$(SOURCES))
BINARY_T  := $(patsubst bins/%.r5o,bins/%.r5o.text.bin,$(BINS))
BINARY_D  := $(patsubst bins/%.r5o,bins/%.r5o.data.bin,$(BINS))

.PHONY: all
all: $(BINS) $(DUMPS) $(BINARY_T) $(BINARY_D)

bins/%.r5o: asms/%.s
	mkdir -p bins
	$(RISCV)gcc $< $(RISCV_GCC_OPTS) -o $@ 
	
#bins/%.r5o.bin: bins/%.r5o
#	mkdir -p bins
#	 $(RISCV)objcopy -O binary $< $@	

bins/%.r5o.text.bin: bins/%.r5o
	mkdir -p bins
	$(RISCV)objcopy -j .text -O binary $< $@
	 
bins/%.r5o.data.bin: bins/%.r5o
	mkdir -p bins
	$(RISCV)objcopy -j .data -O binary $< $@
	 
dumps/%.r5o.dump: bins/%.r5o
	mkdir -p dumps
	$(RISCV)objdump -j .text -j .data -d $< > $@

.PHONY: run_all
run_all: $(RUNS)

runs/%: bins/%.r5o
	mkdir -p runs
	spike --steps=2000  --log-commits --isa=rv32ima_zicsr --priv=msu  -l $< 2> $@.iss


.PHONY: clean
clean:
	rm -rf bins dumps runs

