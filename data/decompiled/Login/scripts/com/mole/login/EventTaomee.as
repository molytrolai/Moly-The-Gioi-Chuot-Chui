package com.mole.login
{
   import flash.events.Event;
   
   public class EventTaomee extends Event
   {
      
      public var EventObj:Object;
      
      public function EventTaomee(param1:String, param2:Object = null, param3:Boolean = false, param4:Boolean = false)
      {
         super(param1,param3,param4);
         this.EventObj = param2;
      }
      
      override public function clone() : Event
      {
         return new EventTaomee(type,this.EventObj,bubbles,cancelable);
      }
   }
}

