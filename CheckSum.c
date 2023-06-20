unsigned char Copy_u8BufData [50] = {':','1','0','0','0','0','0','0','0','0','0','5','0','0','0','2','0','2','1','0','2','0','0','0','8','2','7','0','2','0','0','0','8','2','B','0','2','0','0','0','8','E','F','\n'};
 unsigned char AsciToHex(unsigned char Copy_u8Asci)
{
	unsigned char Result;
	if ( (Copy_u8Asci >= 48) && (Copy_u8Asci <= 57) )
	{
		Result = Copy_u8Asci - 48;
	}

	else
	{
		Result = Copy_u8Asci - 55;
	}

	return Result;
}
int main() {
    // Write C code here
      unsigned char i =1;
    unsigned short int result = 0 ;
     unsigned char  digitCount = 1 ;
    while(Copy_u8BufData[i+2]!= '\n')
    {
       
          Copy_u8BufData[i] = AsciToHex(Copy_u8BufData[i]);
            Copy_u8BufData[i+1] = AsciToHex(Copy_u8BufData[i+1]);
        
        result += (Copy_u8BufData[i]<<4|Copy_u8BufData[i+1]) ;
      
        i+=2;
      
        digitCount+=2 ;

        
         
    }
    digitCount+=2;
  
     Copy_u8BufData[digitCount-2] = AsciToHex( Copy_u8BufData[digitCount-2]);
    Copy_u8BufData[digitCount-1] = AsciToHex( Copy_u8BufData[digitCount-1]);
 
   //checksum calculations 
   result &= 0xff ; // to get the lowest byte
    
   result = ((unsigned char)(~result))+1 ; // twos complment
    
    unsigned char checksum = (Copy_u8BufData[digitCount-2]<<4|Copy_u8BufData[digitCount-1]) ;
   
   if(result != checksum)
   {
       //return 0 ;
       printf(" %d",0);
   }
   else {
         printf("%d",1);
   }
   
  
    return 0;
}