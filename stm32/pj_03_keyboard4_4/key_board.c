#include "stm32f10x.h"
#include "delay.h"
#include "key_board.h"


//uint8_t Send_F=0;


void Keyboard_GPIO_Config(void)
{
    GPIO_InitTypeDef  GPIO_InitStruct;
    
    KEYBOARD_GPIO_CLK_FUN(KEYBOARD_GPIO_CLK,ENABLE);
    
    //LINE    
    GPIO_InitStruct.GPIO_Pin=KEYBOARD_GPIO_PIN0|KEYBOARD_GPIO_PIN1|KEYBOARD_GPIO_PIN2|KEYBOARD_GPIO_PIN3;
    GPIO_InitStruct.GPIO_Mode=GPIO_Mode_Out_PP;
    GPIO_InitStruct.GPIO_Speed=GPIO_Speed_10MHz;
    GPIO_Init(KEYBOARD_GPIO_PORT,&GPIO_InitStruct);

    //ROW
    GPIO_InitStruct.GPIO_Pin=KEYBOARD_GPIO_PIN4|KEYBOARD_GPIO_PIN5|KEYBOARD_GPIO_PIN6|KEYBOARD_GPIO_PIN7;
    GPIO_InitStruct.GPIO_Mode=GPIO_Mode_IPU;
    GPIO_InitStruct.GPIO_Speed=GPIO_Speed_10MHz;
    GPIO_Init(KEYBOARD_GPIO_PORT,&GPIO_InitStruct);
}

uint16_t keyboard_scan(void)
{
    uint16_t key_val=0;
    uint16_t temp=0;
	
	
	/*************Scan  1st Line************************/

    GPIOD->ODR=0X00;

    GPIOD->ODR=0XF7;

    if((GPIOD->IDR&0XF0)!=0XF0)
    {
        delay_ms(50);

        if((GPIOD->IDR & 0XF0)!=0XF0)
        {
            temp=(GPIOD->IDR&0XF7);
            switch(temp)
            {
                case 0xE7:  key_val=1;   break;

                case 0xD7:  key_val=2;   break;

                case 0xB7:  key_val=3;   break;

                case 0x77:  key_val=4;   break;

                default:    key_val=0;   break;
            }
        }
    }
    
		/*************Scan  2st Line************************/
    GPIOD->ODR=0X00;

    GPIOD->ODR=0XFB;

    if((GPIOD->IDR&0XF0)!=0XF0)
    {
        delay_ms(50);

        if((GPIOD->IDR & 0XF0)!=0XF0)
        {
            temp=(GPIOD->IDR&0XFB);
            switch(temp)
            {
                case 0xEB:  key_val=5;  break;

                case 0xDB:  key_val=6;  break;

                case 0xBB:  key_val=7;  break;

                case 0x7B:  key_val=8;  break;

                default:    key_val=0;  break;
            }
        }
    }

		/*************Scan  3st Line************************/
    GPIOD->ODR=0X00;

    GPIOD->ODR=0XFD;

    if((GPIOD->IDR&0XF0)!=0XF0)
    {
        delay_ms(50);

        if((GPIOD->IDR & 0XF0)!=0XF0)
        {
            temp=(GPIOD->IDR&0XFD);
            switch(temp)
            {
                case 0xED:  key_val=9;   break;

                case 0xDD:  key_val=10;  break;

                case 0xBD:  key_val=11;  break;

                case 0x7D:  key_val=12;  break;

                default:    key_val=0;   break;
            }
        }
    }

		/*************Scan  4st Line************************/
    GPIOD->ODR=0X00;

    GPIOD->ODR=0XFE;

    if((GPIOD->IDR&0XF0)!=0XF0)
    {
        delay_ms(50);

        if((GPIOD->IDR & 0XF0)!=0XF0)
        {
            temp=(GPIOD->IDR&0XFE);
            switch(temp)
            {
                case 0xEE:  key_val=13;  break;

                case 0xDE:  key_val=14;  break;

                case 0xBE:  key_val=15;  break;

                case 0x7E:  key_val=16;  break;

                default:    key_val=0;   break;
            }
        }
    }

    return key_val;

}
