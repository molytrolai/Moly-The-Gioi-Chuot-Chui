package org.taomee.register
{
   import flash.display.Bitmap;
   import flash.display.Sprite;
   import flash.events.MouseEvent;
   import org.taomee.register.event.CaptchaEvent;
   
   public class CaptchaComponent extends Sprite
   {
      
      private var captchaBitmap:Bitmap;
      
      public function CaptchaComponent(param1:Boolean = true)
      {
         super();
         RegisterControl.instance.addEventListener(CaptchaEvent.REGISTER_CAPTCHA_RECEIVED,this.onCaptchaReceived);
         buttonMode = true;
         if(param1)
         {
            addEventListener(MouseEvent.CLICK,this.onClick);
         }
      }
      
      public function refreshCaptcha() : void
      {
         mouseEnabled = false;
         RegisterControl.instance.requestCaptcha();
      }
      
      private function onClick(param1:MouseEvent) : void
      {
         this.refreshCaptcha();
      }
      
      private function onCaptchaReceived(param1:CaptchaEvent) : void
      {
         mouseEnabled = true;
         if(Boolean(this.captchaBitmap) && contains(this.captchaBitmap))
         {
            removeChild(this.captchaBitmap);
         }
         this.captchaBitmap = param1.captchaBitmap;
         addChild(this.captchaBitmap);
      }
   }
}

