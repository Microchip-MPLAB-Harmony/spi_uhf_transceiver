/* Function:
    void delay_ms(uint32_t ms)

  Summary:
    Delays program execution for a dedicated time.

  Description:
    This function delays program execution for a dedicated time in ms. Systick
    periheral is used for delay generation.

  Remarks:
    Systick peripheral in Time system service has to be enabled.
*/
extern void delay_ms(uint32_t);

/* Function:
    void delay_us(uint32_t us)

  Summary:
    Delays program execution for a dedicated time.

  Description:
    This function delays program execution for a dedicated time in us. Systick
    periheral is used for delay generation.

  Remarks:
    Systick peripheral in Time system service has to be enabled.
*/
extern void delay_us(uint32_t);