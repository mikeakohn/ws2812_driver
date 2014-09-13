;; LED Panel - Copyright 2014 by Michael Kohn
;; Email: mike@mikekohn.net
;;   Web: http://www.mikekohn.net/
;;
;; Control a string of LED's controlled by a WS2812 controller.

.include "tn85def.inc"
.avr8

; CKSEL = 0001
; CLKPS = 0000
; CKDIV8 = 0
;
; FUSE EXTD = 0xff
; FUSE HIGH = 0xdf
; FUSE LOW =  0xc1

; 9600 Baud: 20,000,000 * (1 / 9600) = 2083 cycles or when timer is 255
;                                      ticks * 8, 8 interrupts

RX_PIN equ 0
TX_PIN equ 1
DATA_OUT equ 2

; r0  = 0
; r1  = 1
; r15 = 255
; r14 = temp
; r16 = paramter to function
; r17 = temp
; r18 =
; r19 = 
; r20 = count in interrupt
; r21 =
; r22 =
; r23 =
; r24 =
; r25 =
; r26 =
; r27 =
; r30 =
; r31 =
;

.org 0x000
  rjmp start
.org 0x00a
  rjmp service_interrupt

start:
  ;; Disable interrupts
  cli

  ;; Set up stack ptr
  ;ldi r17, RAMEND>>8
  ;out SPH, r17
  ldi r17, RAMEND&255
  out SPL, r17

  ;; r0 = 0, r1 = 1, r15 = 255
  eor r0, r0
  eor r1, r1
  inc r1
  ldi r17, 0xff
  mov r15, r17

  ;; Set up PORTB
  ;; P0 = RX
  ;; P1 = TX
  ldi r17, (1<<TX_PIN)|(1<<DATA_OUT)
  out DDRB, r17             ; PB0 is input, PB1, PB2 are output
  ldi r17, (1<<TX_PIN)      ; |(1<<DATA_OUT)  (idle low?)
  out PORTB, r17            ; RX is 0, TX is 1

  ;; Set up TIMER0
  ldi r17, 255                   ; with /1 prescale this is 2083 interrupts/s
  out OCR0A, r17

  ldi r17, (1<<OCIE0A)
  out TIMSK, r17                 ; enable interrupt compare A 
  ldi r17, (1<<WGM01)
  out TCCR0A, r17                ; normal counting (0xffff is top, count up)
  ldi r17, (1<<CS00)             ; CTC OCR0A  Clear Timer on Compare
  out TCCR0B, r17                ; prescale = 1 from clock source

  ; Interrupt enable
  sei

  ;ldi r16, 'A'
  ;rcall send_byte
  ;rcall send_temp

  ;; Clear LED RAM (40 * 3 bytes)
  ldi r28, (SRAM_START)&0xff
  ldi r29, (SRAM_START)>>8
  ldi r23, 120 
memset:
  st Y+, r0
  dec r23
  brne memset

  ;ldi r23, 0xff
  ;sts SRAM_START, r23
  ;ldi r23, 128
  ;sts SRAM_START+4, r23

  ;rcall send_ready

main:
  sbic PINB, RX_PIN
  rjmp main

  rcall read_byte
  cpi r16, 0xff
  breq parse_command

  ;; pixel#, r, g, b
  mov r19, r16
  rcall read_rgb

  mov r6, r19
  add r19, r6
  add r19, r6
  ldi r28, (SRAM_START)&0xff
  ldi r29, (SRAM_START)>>8
  add r28, r19
  adc r29, r0
  st Y+, r11
  st Y+, r10
  st Y+, r12

  ;rcall send_led_data
  ldi r16, '*'
  rcall send_byte
  rjmp main

parse_command:
  ;ldi r16, '?'
  ;rcall send_byte
  rcall read_byte

  cpi r16, 0xff
  brne not_ff
  rcall send_led_data
  rjmp parse_command_exit
not_ff:

  cpi r16, 0xfe
  brne not_fe
  rcall set_all
  rjmp parse_command_exit
not_fe:

  cpi r16, 0xfd
  brne not_fd
  rcall shift_left_linear
  rjmp parse_command_exit
not_fd:

  cpi r16, 0xfc
  brne not_fc
  rcall shift_right_linear
  rjmp parse_command_exit
not_fc:

parse_command_exit: 
  ldi r16, '*'
  rcall send_byte
  rjmp main

;; Set all pixels to RGB (r7, r8, r9)
set_all:
  rcall read_rgb
  ldi r28, (SRAM_START)&0xff
  ldi r29, (SRAM_START)>>8
  ldi r23, 40 
set_all_loop:
  st Y+, r11
  st Y+, r10
  st Y+, r12
  dec r23
  brne set_all_loop
  ret

shift_left_linear:
  ldi r28, (SRAM_START)&0xff
  ldi r29, (SRAM_START)>>8
  ldi r30, (SRAM_START)&0xff
  ldi r31, (SRAM_START)>>8
  adiw r30, 3
  ldi r23, 120-3 
shift_left_linear_loop:
  ld r11, Z+
  st Y+, r11
  dec r23
  brne shift_left_linear_loop
  st Y+, r0
  st Y+, r0
  st Y+, r0
  ret

shift_right_linear:
  ldi r28, (SRAM_START)&0xff
  ldi r29, (SRAM_START)>>8
  ldi r30, (SRAM_START)&0xff
  ldi r31, (SRAM_START)>>8
  adiw r30, 60
  adiw r30, 60-3
  adiw r28, 60 
  adiw r28, 60 
  ldi r23, 120-3 
shift_right_linear_loop:
  ld r11, -Z 
  st -Y, r11
  dec r23
  brne shift_right_linear_loop
  st -Y, r0
  st -Y, r0
  st -Y, r0
  ret

read_rgb:
  rcall read_byte
  mov r10, r16 
  rcall read_byte
  mov r11, r16
  rcall read_byte
  mov r12, r16 
  ret

send_led_data:
  ;; Y points to LED data, r23 counts 120 bytes
  ldi r28, (SRAM_START)&0xff
  ldi r29, (SRAM_START)>>8
  ldi r23, 120        ; byte_count = 120

  cli     ; No interrupts while sending LED data

  ;; Send LED data
next_byte:
  ld r16, Y+
  ldi r17, 8
next_bit:
  ;; 0: T0H=0.35us  T0L=0.8us   @20MHz 7 cycles  / 16 cycles
  ;; 1: T1H=0.70us  T1L=0.6us   @20MHz 14 cycles / 12 cycles
  sbi PORTB, DATA_OUT
  sbrc r16, 7
  rjmp t1h
t0h:
  ;nop               ; sbrc=2 (skip +1), nop=1, rjmp=2, cbi PORTB=2 (7 cycles)
  rjmp end_bit_on
t1h:
  nop               ; sbrc=1, rjmp=2, nop*9=9, cbi PORTB=2 (14 cycles)
  nop
  nop
  nop
  nop
  nop
  nop
  nop
  nop
end_bit_on:
  cbi PORTB, DATA_OUT

  sbrc r16, 7       ; 2 cycles if skipped, 1 cycle otherwise
  rjmp t1l          ; 2 cycles
t0l:
  nop               ; sbrc=2, nop*8=6, rjmp=2, lsl=1,dec=1,brne=2,sbi PORT=2
  nop
  nop
  nop
  nop
  nop
  rjmp end_bit_off
t1l:
  nop               ; sbrc=1,rjmp=2, nop*2=3, lsl=1,dec=1,brne=2,sbi PORT=2
  nop
  nop
end_bit_off:
  lsl r16           ; 1 cycle

  dec r17           ; bit_count--;   1 cycle
  brne next_bit     ;                2 cycle if branch taken (otherwise 1)
  dec r23           ; byte_count--;  1 cycle
  brne next_byte    ;                2 cycle if branch taken (otherwise 1)

  sbi PORTB, DATA_OUT

  sei     ; Turn interrupts back on

  cbi PORTB, DATA_OUT
  ;; End by sending a reset pulse
  out TCNT0, r0
  clr r20
  cbi PORTB, DATA_OUT 
wait_reset_pulse_end:
  cpi r20, 4 
  brne wait_reset_pulse_end
  ;sbi PORTB, DATA_OUT

  ret

;; send_ready
send_ready:
  ldi r30, (ready * 2) & 0xff
  ldi r31, (ready * 2) >> 8
  rcall send_string
  ret

;; send_string(Z)
send_string:
  lpm r16, Z+
  cpi r16, 0
  breq send_string_exit
  rcall send_byte
  rjmp send_string
send_string_exit:
  ret

;; send_byte(r16) Software UART
send_byte:
  ; with /1 prescale this is 255 ticks for an interrupt * 8, approx 1/9600
  ;ldi r17, 255
  ;out OCR0A, r17

  ;; Start bit is 0
  out TCNT0, r0
  clr r20
  cbi PORTB, TX_PIN 
wait_start_bit:
  cpi r20, 8 
  brne wait_start_bit

  ;; Shift out 8 bit LSb first + start bit
  ldi r17, 9
shift_next_bit:
  out TCNT0, r0
  sbrc r16, 0
  sbi PORTB, TX_PIN 
  sbrs r16, 0
  cbi PORTB, TX_PIN 
  sec
  ror r16
  clr r20
wait_data_bit:
  cpi r20, 8
  brne wait_data_bit
  dec r17
  brne shift_next_bit
  ret

;; read_byte(r16) Software UART
read_byte:
  ;; Wait for data
  sbic PINB, RX_PIN
  rjmp read_byte

  ; with /1 prescale this is 255 ticks for an interrupt * 8, approx 1/9600
  ; Wait 1.5 bits (full start bit + 1/2 of the first data bit so we
  ; sample in the center of all 8 bits
  ;ldi r17, 255
  ;out OCR0A, r17

  ;; Start bit is 0
  out TCNT0, r0
  clr r20
wait_start_bit_in:
  cpi r20, 12 
  brne wait_start_bit_in

  ;; Shift out 8 bit LSb first + start bit
  ldi r16, 0      ; store result in r16
  ldi r17, 8      ; ignore the stop bit, read 8 bits
shift_next_bit_in:
  out TCNT0, r0   ; reset timer
  clr r20

  sbic PINB, RX_PIN ; if we read 1 from input pin, carry=1 else carry=0
  sec
  sbis PINB, RX_PIN 
  clc
  ror r16         ; roll right with carry

wait_data_bit_in:
  cpi r20, 8
  brne wait_data_bit_in
  dec r17
  brne shift_next_bit_in

  sbi DDRB, TX_PIN 
  ret

service_interrupt:
  in r7, SREG
  inc r20
exit_interrupt:
  out SREG, r7
  reti

.align 16
ready:
.db "ready\r\n", 0

.align 16
signature:
.db "LED Panel - Copyright 2014 - Michael Kohn - Version 0.01",0



