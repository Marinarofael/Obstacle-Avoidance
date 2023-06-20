
#include "STD_TYPES.h"
#include "BIT_MATH.h"
#include "USART_interface.h"
#include "RCC_interface.h"
#include "motor.h"


/* Creating flag to be in specific section*/
__attribute__ ((section(".flag_section_comp"),used))
FlagStatus_t flag = FlagStatus_enuWaitStart;
/*Creating marker to be in specific section*/
__attribute__ ((section(".marker_section_comp"),used))
MarkerStatus_t APPmarker = MarkerStatus_enuNoApplication;


volatile u8  u8SystemOrder   = 0;


Motor_init();
while(1)
{
    while(MUSART1_u8Receive( &u8SystemOrder ) == 0) // while nothing is received , keep moving the car
    {
            Motor_Forward(&motor_one) ;
            Motor_Forward(&motor_two) ;
            Motor_Forward(&motor_three) ;
            Motor_Forward(&motor_four) ;
    }
    if(u8SystemOrder == 'c') // if an obstacle is detected
		{
			 Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);

		}
     if(u8SystemOrder == 'e') // if a stop signal is sent
		{
			 Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);
            // flag = wait start
            // update marker
             //reset

		}

         if(u8SystemOrder == 'f') // if a stop signal is sent
		{
			 Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);
             Motor_Stop(motor_t * motor);
            // flag =need start
            // update marker
             //reset

		}
}