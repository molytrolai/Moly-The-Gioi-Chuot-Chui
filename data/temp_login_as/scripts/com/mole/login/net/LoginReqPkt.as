package com.mole.login.net
{
   import com.mole.login.*;
   import com.mole.login.type.*;
   import flash.utils.*;
   
   public class LoginReqPkt
   {
      
      private static const PacketHeadLength:uint = 17;
      
      public function LoginReqPkt()
      {
         super();
      }
      
      public static function pack(param1:uint, param2:uint, param3:ByteArray = null) : ByteArray
      {
         if(Boolean(param3) && (param2 == LoginCmd.CMD_LOGIN || param2 == LoginCmd.CMD_CREATE_MOLE))
         {
            param3.writeBytes(LoginData.getAdByte());
         }
         var _loc4_:ByteArray = packBody(param3);
         var _loc5_:ByteArray = packHead(param1,param2,_loc4_.length);
         var _loc6_:ByteArray = new ByteArray();
         _loc6_.writeBytes(_loc5_);
         _loc6_.writeBytes(_loc4_);
         return _loc6_;
      }
      
      private static function packBody(param1:ByteArray) : ByteArray
      {
         var _loc2_:ByteArray = new ByteArray();
         if(param1)
         {
            _loc2_.writeBytes(param1);
         }
         return _loc2_;
      }
      
      private static function packHead(param1:uint, param2:uint, param3:int) : ByteArray
      {
         var _loc4_:ByteArray = new ByteArray();
         _loc4_.writeUnsignedInt(PacketHeadLength + param3);
         _loc4_.writeByte(1);
         _loc4_.writeUnsignedInt(param2);
         _loc4_.writeUnsignedInt(param1);
         _loc4_.writeInt(0);
         return _loc4_;
      }
   }
}

