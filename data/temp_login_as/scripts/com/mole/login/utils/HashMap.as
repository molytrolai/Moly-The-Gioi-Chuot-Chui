package com.mole.login.utils
{
   import flash.utils.*;
   
   public class HashMap
   {
      
      private var _length:int;
      
      private var _weakKeys:Boolean;
      
      private var _content:Dictionary;
      
      public function HashMap(param1:Boolean = false)
      {
         super();
         this._weakKeys = param1;
         this._length = 0;
         this._content = new Dictionary(param1);
      }
      
      public function containsKey(param1:*) : Boolean
      {
         if(param1 in this._content)
         {
            return true;
         }
         return false;
      }
      
      public function getValue(param1:*) : *
      {
         var _loc2_:* = this._content[param1];
         return _loc2_ == undefined ? null : _loc2_;
      }
      
      public function remove(param1:*) : *
      {
         if(!(param1 in this._content))
         {
            return null;
         }
         var _loc2_:* = this._content[param1];
         delete this._content[param1];
         --this._length;
         return _loc2_;
      }
      
      public function get weakKeys() : Boolean
      {
         return this._weakKeys;
      }
      
      public function clear() : void
      {
         this._length = 0;
         this._content = new Dictionary(this._weakKeys);
      }
      
      public function containsValue(param1:*) : Boolean
      {
         var _loc2_:* = undefined;
         for each(_loc2_ in this._content)
         {
            if(_loc2_ === param1)
            {
               return true;
            }
         }
         return false;
      }
      
      public function get values() : Array
      {
         var _loc1_:* = undefined;
         var _loc2_:Array = new Array(this._length);
         var _loc3_:* = 0;
         for each(_loc1_ in this._content)
         {
            var _loc6_:Number;
            _loc2_[_loc6_ = _loc3_++] = _loc1_;
         }
         return _loc2_;
      }
      
      public function clone() : HashMap
      {
         var _loc1_:* = undefined;
         var _loc2_:HashMap = new HashMap(this._weakKeys);
         for(_loc1_ in this._content)
         {
            _loc2_.add(_loc1_,this._content[_loc1_]);
         }
         return _loc2_;
      }
      
      public function add(param1:*, param2:*) : *
      {
         var _loc3_:* = undefined;
         if(param1 == null)
         {
            throw new ArgumentError("cannot put a value with undefined or null key!");
         }
         if(param2 == null)
         {
            return null;
         }
         if(!(param1 in this._content))
         {
            ++this._length;
         }
         _loc3_ = this.getValue(param1);
         this._content[param1] = param2;
         return _loc3_;
      }
      
      public function isEmpty() : Boolean
      {
         return this._length == 0;
      }
      
      public function get length() : int
      {
         return this._length;
      }
      
      public function getKey(param1:*) : *
      {
         var _loc2_:* = undefined;
         for(_loc2_ in this._content)
         {
            if(this._content[_loc2_] == param1)
            {
               return _loc2_;
            }
         }
         return null;
      }
      
      public function get keys() : Array
      {
         var _loc1_:* = undefined;
         var _loc2_:Array = new Array(this._length);
         var _loc3_:* = 0;
         for(_loc1_ in this._content)
         {
            var _loc6_:Number;
            _loc2_[_loc6_ = _loc3_++] = _loc1_;
         }
         return _loc2_;
      }
      
      public function combine(param1:HashMap) : void
      {
         var _loc2_:Array = null;
         var _loc3_:* = undefined;
         if(param1)
         {
            _loc2_ = param1.keys;
            for each(_loc3_ in _loc2_)
            {
               this.add(_loc3_,param1.getValue(_loc3_));
            }
         }
      }
      
      public function toString() : String
      {
         var _loc1_:* = 0;
         var _loc2_:Array = this.keys;
         var _loc3_:Array = this.values;
         var _loc4_:uint = _loc2_.length;
         var _loc5_:String = "HashMap-----------------------------------------------------";
         _loc1_ = 0;
         while(_loc1_++ < _loc4_)
         {
            _loc5_ += _loc2_[_loc1_] + " -> " + _loc3_[_loc1_] + "\n";
         }
         return _loc5_ + "-----------------------------------------------------";
      }
   }
}

