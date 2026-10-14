package
{
   import flash.display.MovieClip;
   import flash.display.SimpleButton;
   import flash.events.MouseEvent;
   import flash.net.URLRequest;
   import flash.net.navigateToURL;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol239")]
   public dynamic class RES_Login_Panel extends MovieClip
   {
      
      public var bbs_btn:SimpleButton;
      
      public var collect_btn:SimpleButton;
      
      public var login_btn:SimpleButton;
      
      public var intro_btn:SimpleButton;
      
      public var taomeeGame_btn:SimpleButton;
      
      public var famknow_btn:SimpleButton;
      
      public var create_btn:SimpleButton;
      
      public function RES_Login_Panel()
      {
         super();
         addFrameScript(0,frame1);
      }
      
      public function gotoTaomeeGame(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("http://game.61.com"),"_blank");
      }
      
      internal function frame1() : *
      {
         taomeeGame_btn.addEventListener(MouseEvent.CLICK,gotoTaomeeGame);
      }
   }
}

