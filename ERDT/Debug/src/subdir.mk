################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/main.c \
../src/syscalls.c \
../src/system_stm32f30x.c 

OBJS += \
./src/main.o \
./src/syscalls.o \
./src/system_stm32f30x.o 

C_DEPS += \
./src/main.d \
./src/syscalls.d \
./src/system_stm32f30x.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -DSTM32 -DSTM32F3 -DSTM32F30 -DSTM32F303VCTx -DSTM32F3DISCOVERY -DDEBUG -DSTM32F303xC -DUSE_STDPERIPH_DRIVER -I"/home/tony/workspace/hillaasist/Utilities" -I"/home/tony/workspace/hillaasist/StdPeriph_Driver/inc" -I"/home/tony/workspace/hillaasist/inc" -I"/home/tony/workspace/hillaasist/CMSIS/device" -I"/home/tony/workspace/hillaasist/CMSIS/core" -O0 -g3 -Wall -fmessage-length=0 -ffunction-sections -c -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


