package com.mole.login.utils
{
   import flash.utils.*;
   
   public class RegCipher
   {
      
      private var _regCipher:Dictionary;
      
      public function RegCipher()
      {
         super();
         this._regCipher = new Dictionary();
         this._regCipher["123456"] = true;
         this._regCipher["123456789"] = true;
         this._regCipher["111111"] = true;
         this._regCipher["123123"] = true;
         this._regCipher["1234567890"] = true;
         this._regCipher["000000"] = true;
         this._regCipher["123321"] = true;
         this._regCipher["zxcvbnm"] = true;
         this._regCipher["1234567"] = true;
         this._regCipher["qwertyuiop"] = true;
         this._regCipher["789456123"] = true;
         this._regCipher["asdfghjkl"] = true;
         this._regCipher["789456"] = true;
         this._regCipher["147258369"] = true;
         this._regCipher["741852963"] = true;
         this._regCipher["123123123"] = true;
         this._regCipher["112233"] = true;
         this._regCipher["qwerty"] = true;
         this._regCipher["987654321"] = true;
         this._regCipher["asdfgh"] = true;
         this._regCipher["12345678910"] = true;
         this._regCipher["456123"] = true;
         this._regCipher["555555"] = true;
         this._regCipher["12345678"] = true;
         this._regCipher["qazwsx"] = true;
         this._regCipher["666666"] = true;
         this._regCipher["159753"] = true;
         this._regCipher["7758258"] = true;
         this._regCipher["121212"] = true;
         this._regCipher["147258"] = true;
         this._regCipher["aaaaaa"] = true;
         this._regCipher["123654"] = true;
         this._regCipher["159357"] = true;
         this._regCipher["zxcvbn"] = true;
         this._regCipher["qazwsxedc"] = true;
         this._regCipher["222222"] = true;
         this._regCipher["0123456789"] = true;
         this._regCipher["963852741"] = true;
         this._regCipher["1233211234567"] = true;
         this._regCipher["1234560"] = true;
         this._regCipher["5201314"] = true;
         this._regCipher["456789"] = true;
         this._regCipher["333333"] = true;
         this._regCipher["123789"] = true;
         this._regCipher["1111111"] = true;
         this._regCipher["123654789"] = true;
         this._regCipher["654321"] = true;
         this._regCipher["741852"] = true;
         this._regCipher["7894561230"] = true;
         this._regCipher["888888"] = true;
         this._regCipher["147852369"] = true;
         this._regCipher["asdasd"] = true;
      }
      
      public function check(param1:String) : Boolean
      {
         return this._regCipher[param1];
      }
   }
}

