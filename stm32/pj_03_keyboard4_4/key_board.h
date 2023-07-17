#include "stm32f10x.h"

#ifndef     _KEY_BOARD_H_
#define     _KEY_BOARD_H_



#define   KEYBOARD_GPIO_PORT          GPIOD
#define   KEYBOARD_GPIO_CLK_FUN       RCC_APB2PeriphClockCmd
#define   KEYBOARD_GPIO_CLK           RCC_APB2Periph_GPIOD


//line    行
#define   KEYBOARD_GPIO_PIN0           GPIO_Pin_0
#define   KEYBOARD_GPIO_PIN1           GPIO_Pin_1
#define   KEYBOARD_GPIO_PIN2           GPIO_Pin_2
#define   KEYBOARD_GPIO_PIN3           GPIO_Pin_3



//row      列
#define   KEYBOARD_GPIO_PIN4           GPIO_Pin_4
#define   KEYBOARD_GPIO_PIN5           GPIO_Pin_5
#define   KEYBOARD_GPIO_PIN6           GPIO_Pin_6
#define   KEYBOARD_GPIO_PIN7           GPIO_Pin_7



//extern uint8_t Send_F;

extern void Keyboard_GPIO_Config(void);
extern uint16_t keyboard_scan(void);

#endif
