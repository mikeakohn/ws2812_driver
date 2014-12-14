
PROGRAM=ws2812_firmware

default: $(PROGRAM).hex

$(PROGRAM).hex: $(PROGRAM).asm
	naken_asm -l -I../../devkits/atmel -o $(PROGRAM).hex $(PROGRAM).asm

program:
	sudo avrdude -c usbtiny -p t85 -U flash:w:$(PROGRAM).hex:i

setfuse:
	sudo avrdude -c usbtiny -p t85 -U lfuse:w:0xee:m

clean:
	@rm -f *.hex
	@rm -f *.lst
	@echo "Clean!"


