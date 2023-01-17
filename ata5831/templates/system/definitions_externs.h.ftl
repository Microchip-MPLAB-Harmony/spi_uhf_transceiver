/* Function:
    void delay_ms(uint32_t ms)

  Summary:
    Delays program execution for a dedicated time.

  Description:
    This function delays program execution for a dedicated time in ms. System
    Time Service is used for delay generation.

  Remarks:
    System Time has to be configured.
*/
extern void delay_ms(uint32_t);

/* Function:
    void delay_us(uint32_t us)

  Summary:
    Delays program execution for a dedicated time.

  Description:
    This function delays program execution for a dedicated time in us. System
    Time Service is used for delay generation.

  Remarks:
    System Time has to be configured.
*/
extern void delay_us(uint32_t);