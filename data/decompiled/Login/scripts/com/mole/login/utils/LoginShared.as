package com.mole.login.utils
{
   import flash.events.*;
   import flash.net.*;
   
   public class LoginShared
   {
      
      private static var _sharedObj:SharedObject;
      
      public static const LOGIN_DATA:String = "loginData";
      
      public static const LIST:String = "list";
      
      public function LoginShared()
      {
         super();
      }
      
      public static function setup() : void
      {
         getLoginData();
      }
      
      public static function get isRead51Mole() : Boolean
      {
         return getValue("is61Mole");
      }
      
      public static function set isRead51Mole(param1:Boolean) : void
      {
         modify("is61Mole",param1);
      }
      
      private static function analysis(param1:Object) : Object
      {
         var _loc2_:Object = new Object();
         if(param1.id)
         {
            _loc2_.userID = param1.id;
            _loc2_.remID = param1.rid;
            _loc2_.pwd = param1.pwd;
            _loc2_.remPwd = param1.rpwd;
            _loc2_.nick = param1.nickName;
            _loc2_.Family = param1.Family;
            MoleSharedObject.getMoleData(_loc2_.userID).data.clothArray = param1.clothArray;
            return _loc2_;
         }
         return null;
      }
      
      public static function modify(param1:Object, param2:Object) : void
      {
         var key:Object = param1;
         var value:Object = param2;
         _sharedObj.data[key] = value;
         try
         {
            _sharedObj.flush();
         }
         catch(e:Error)
         {
         }
      }
      
      public static function getValue(param1:Object) : *
      {
         if(_sharedObj == null)
         {
            getLoginData();
         }
         return _sharedObj.data[param1];
      }
      
      public static function get loginList() : Array
      {
         return getValue(LIST);
      }
      
      public static function set loginList(param1:Array) : void
      {
         modify(LIST,param1);
      }
      
      public static function getUser(param1:Object) : Object
      {
         var _loc2_:Object = null;
         var _loc3_:Object = null;
         for each(_loc2_ in loginList)
         {
            if(_loc2_.userID == param1)
            {
               return _loc2_;
            }
         }
         _loc3_ = new Object();
         _loc3_.userID = param1;
         return _loc3_;
      }
      
      public static function removeUser(param1:Object) : void
      {
         var _loc3_:Object = null;
         var _loc2_:Array = new Array();
         for each(_loc3_ in loginList)
         {
            if(_loc3_.userID != param1)
            {
               _loc2_.push(_loc3_);
            }
         }
         loginList = _loc2_;
      }
      
      public static function addUser(param1:Object, param2:Object = null) : void
      {
         var _loc4_:* = undefined;
         var _loc7_:Object = null;
         var _loc9_:Object = null;
         var _loc10_:Number = Number(NaN);
         var _loc11_:Object = null;
         var _loc12_:uint = 0;
         var _loc3_:Date = new Date();
         var _loc5_:Array = loginList;
         _loc5_ = _loc5_ == null ? [] : _loc5_;
         var _loc6_:int = -1;
         var _loc8_:uint = 0;
         while(_loc8_ < _loc5_.length)
         {
            _loc7_ = _loc5_[_loc8_];
            if(_loc7_.userCode)
            {
               if(_loc7_.userCode == param1.userCode || _loc7_.userID == param1.userID)
               {
                  _loc6_ = int(_loc8_);
                  if(param1.time > _loc7_.time)
                  {
                     for(_loc4_ in param1)
                     {
                        _loc7_[_loc4_] = param1[_loc4_];
                     }
                  }
                  _loc7_.time = _loc3_.time;
                  break;
               }
            }
            else if(_loc7_.userID == param1.userID)
            {
               _loc6_ = int(_loc8_);
               if(param1.time > _loc7_.time)
               {
                  for(_loc4_ in param1)
                  {
                     _loc7_[_loc4_] = param1[_loc4_];
                  }
               }
               _loc7_.time = _loc3_.time;
               break;
            }
            _loc8_++;
         }
         if(_loc6_ == -1)
         {
            param1.time = _loc3_.time;
            _loc5_.push(param1);
            if(param2)
            {
               _loc9_ = MoleSharedObject.getMoleData(param1.userID).data;
               for(_loc4_ in param2)
               {
                  _loc9_[_loc4_] = param2[_loc4_];
               }
            }
         }
         while(_loc5_.length > 5)
         {
            _loc10_ = _loc3_.time;
            _loc12_ = 0;
            while(_loc12_ < _loc5_.length)
            {
               _loc11_ = _loc5_[_loc12_];
               if(_loc11_.time < _loc10_)
               {
                  _loc10_ = Number(_loc11_.time);
                  _loc6_ = int(_loc12_);
               }
               _loc12_++;
            }
            _loc5_.splice(_loc6_,1);
         }
         loginList = _loc5_;
      }
      
      public static function getLoginData() : Object
      {
         if(_sharedObj == null)
         {
            _sharedObj = SharedObject.getLocal("mole/login","/");
            _sharedObj.addEventListener(NetStatusEvent.NET_STATUS,onSOFail);
            _sharedObj.addEventListener(AsyncErrorEvent.ASYNC_ERROR,onSOFail);
         }
         return _sharedObj.data;
      }
      
      private static function onSOFail(param1:Event) : void
      {
      }
   }
}

