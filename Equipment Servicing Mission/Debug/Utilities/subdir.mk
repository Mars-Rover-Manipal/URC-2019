################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Utilities/stm32f3_discovery.c \
../Utilities/stm32f3_discovery_l3gd20.c \
../Utilities/stm32f3_discovery_lsm303dlhc.c 

OBJS += \
./Utilities/stm32f3_discovery.o \
./Utilities/stm32f3_discovery_l3gd20.o \
./Utilities/stm32f3_discovery_lsm303dlhc.o 

C_DEPS += \
./Utilities/stm32f3_discovery.d \
./Utilities/stm32f3_discovery_l3gd20.d \
./Utilities/stm32f3_discovery_lsm303dlhc.d 


# Each subdirectory must supply rules for building sources it contributes
Utilities/%.o: ../Utilities/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -DSTM32 -DSTM32F3 -DSTM32F30 -DSTM32F303VCTx -DSTM32F3DISCOVERY -DDEBUG -DSTM32F303xC -DUSE_STDPERIPH_DRIVER -I"/home/tony/workspace/Motor_Code/Utilities" -I"/home/tony/workspace/Motor_Code/StdPeriph_Driver/inc" -I"/home/tony/workspace/Motor_Code/inc" -I"/home/tony/workspace/Motor_Code/CMSIS/device" -I"/home/tony/workspace/Motor_Code/CMSIS/core" -O0 -g3 -Wall -fmessage-length=0 -ffunction-sections -c -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


