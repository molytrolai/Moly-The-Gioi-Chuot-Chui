package com.mole.login.net
{
   import flash.utils.*;
   
   public class LoginResPkt
   {
      
      public static const HEAD_LENGTH:int = 17;
      
      private var _length:uint;
      
      private var _version:uint;
      
      private var _cmdID:uint;
      
      private var _userId:uint;
      
      private var _seq:uint;
      
      private var _errorID:uint;
      
      private var _bodyData:ByteArray;
      
      public function LoginResPkt(param1:ByteArray)
      {
         super();
         this.parseHead(param1);
         this.parseBody(param1);
      }
      
      public function get length() : uint
      {
         return this._length;
      }
      
      private function parseHead(param1:ByteArray) : void
      {
         this._length = param1.readUnsignedInt();
         this._version = param1.readUnsignedByte();
         this._cmdID = param1.readUnsignedInt();
         this._userId = param1.readUnsignedInt();
         this._errorID = param1.readUnsignedInt();
      }
      
      private function parseBody(param1:ByteArray) : void
      {
         this._bodyData = new ByteArray();
         param1.readBytes(this._bodyData,0,this._length - HEAD_LENGTH);
      }
      
      public function getBody() : ByteArray
      {
         return this._bodyData;
      }
      
      public function get version() : uint
      {
         return this._version;
      }
      
      public function get cmdID() : uint
      {
         return this._cmdID;
      }
      
      public function get userID() : uint
      {
         return this._userId;
      }
      
      public function get seq() : uint
      {
         return this._seq;
      }
      
      public function get errorID() : uint
      {
         return this._errorID;
      }
   }
}

