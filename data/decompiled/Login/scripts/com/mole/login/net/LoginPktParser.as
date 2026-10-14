package com.mole.login.net
{
   import com.adobe.crypto.*;
   import com.mole.login.*;
   import com.mole.login.type.*;
   import com.mole.login.utils.*;
   import flash.utils.*;
   
   public class LoginPktParser
   {
      
      public function LoginPktParser()
      {
         super();
      }
      
      public static function GetAuthCode() : void
      {
         var _loc1_:ByteArray = LoginReqPkt.pack(0,LoginCmd.CMD_GET_AUTHCODE);
         LoginSocket.instance.send(_loc1_);
      }
      
      public static function IdLogin(param1:uint, param2:String, param3:Object) : void
      {
         var _loc4_:ByteArray = new ByteArray();
         if(param2.length == 32)
         {
            _loc4_.writeUTFBytes(param2);
         }
         else
         {
            _loc4_.writeUTFBytes(MD5.hash(MD5.hash(param2)));
         }
         _loc4_.writeUnsignedInt(LoginData.loginType);
         _loc4_.writeUnsignedInt(1);
         _loc4_.writeUnsignedInt(0);
         var _loc5_:ByteArray = new ByteArray();
         if(param3 == null)
         {
            _loc5_.length = 22;
            _loc5_.position = 0;
         }
         else
         {
            param3.codeId.position = 0;
            _loc5_.writeBytes(param3.codeId);
            _loc5_.writeUTFBytes(param3.value);
            _loc5_.length = 22;
         }
         _loc4_.writeBytes(_loc5_);
         var _loc6_:ByteArray = LoginReqPkt.pack(param1,LoginCmd.CMD_LOGIN,_loc4_);
         LoginSocket.instance.send(_loc6_);
         LoginDebug.inst.write("ID号登录：ID:" + param1 + "    Pwd:" + param2 + "CmdID:" + LoginCmd.CMD_LOGIN);
      }
      
      public static function EmailLogin(param1:String, param2:String, param3:Object = null) : void
      {
         var _loc4_:ByteArray = new ByteArray();
         _loc4_.writeBytes(LoginUtil.FillString(param1,64));
         if(param2.length == 32)
         {
            _loc4_.writeUTFBytes(param2);
         }
         else
         {
            _loc4_.writeUTFBytes(MD5.hash(MD5.hash(param2)));
         }
         _loc4_.writeUnsignedInt(LoginData.loginType);
         _loc4_.writeUnsignedInt(1);
         _loc4_.writeUnsignedInt(0);
         var _loc5_:ByteArray = new ByteArray();
         if(param3 == null)
         {
            _loc5_.length = 22;
            _loc5_.position = 0;
         }
         else
         {
            param3.codeId.position = 0;
            _loc5_.writeBytes(param3.codeId);
            _loc5_.writeUTFBytes(param3.value);
            _loc5_.length = 22;
         }
         _loc4_.writeBytes(_loc5_);
         var _loc6_:ByteArray = LoginReqPkt.pack(0,LoginCmd.CMD_LOGIN,_loc4_);
         LoginSocket.instance.send(_loc6_);
      }
      
      public static function CreateMole() : void
      {
         var _loc1_:ByteArray = new ByteArray();
         _loc1_.writeBytes(LoginData.session);
         _loc1_.writeBytes(LoginUtil.FillString("小摩尔",16));
         _loc1_.writeUnsignedInt(0);
         _loc1_.writeUnsignedInt(LoginData.loginType);
         var _loc2_:ByteArray = LoginReqPkt.pack(LoginData.userID,LoginCmd.CMD_CREATE_MOLE,_loc1_);
         LoginSocket.instance.send(_loc2_);
      }
      
      public static function GetRecomServers() : void
      {
         var _loc1_:ByteArray = new ByteArray();
         _loc1_.writeBytes(LoginData.session);
         _loc1_.writeUnsignedInt(LoginData.loginType);
         var _loc2_:ByteArray = LoginReqPkt.pack(LoginData.userID,LoginCmd.CMD_GET_GOOD_SERVER_LIST,_loc1_);
         LoginSocket.instance.send(_loc2_);
         LoginDebug.inst.write("获取推荐服务器列表-->登陆区道：" + LoginData.loginType + "   UserID:" + LoginData.userID + "   Len:" + LoginData.session.length);
      }
      
      public static function GetAllServers(param1:int, param2:int) : void
      {
         var _loc4_:int = 0;
         var _loc3_:ByteArray = new ByteArray();
         _loc3_.writeUnsignedInt(param1);
         _loc3_.writeUnsignedInt(param2);
         if(Boolean(LoginData.friendList) && LoginData.friendList.length > 0)
         {
            _loc4_ = int(LoginData.friendList.length);
         }
         else
         {
            _loc4_ = 0;
         }
         _loc3_.writeUnsignedInt(_loc4_);
         var _loc5_:int = 0;
         while(_loc5_ < _loc4_)
         {
            _loc3_.writeUnsignedInt(LoginData.friendList[_loc5_].frend);
            _loc5_++;
         }
         var _loc6_:ByteArray = LoginReqPkt.pack(LoginData.userID,LoginCmd.CMD_GET_SERVER_LIST,_loc3_);
         LoginSocket.instance.send(_loc6_);
      }
   }
}

