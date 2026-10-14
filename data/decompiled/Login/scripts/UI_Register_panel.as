package
{
   import flash.display.MovieClip;
   import flash.display.SimpleButton;
   import flash.text.TextField;
   
   [Embed(source="/_assets/assets.swf", symbol="symbol60")]
   public dynamic class UI_Register_panel extends MovieClip
   {
      
      public var passwordTxt:TextField;
      
      public var authCodeErrorTxt:TextField;
      
      public var registerBtn:SimpleButton;
      
      public var repatePasswordTxt:TextField;
      
      public var serviceBtn:SimpleButton;
      
      public var repatePasswordErrorTxt:TextField;
      
      public var passWordErrorTxt:TextField;
      
      public var authCodeTxt:TextField;
      
      public var closeBtn:SimpleButton;
      
      public var comboxMC:QuestionRadioButtonUI;
      
      public var changeCaptchaBtn:SimpleButton;
      
      public var agreeTxt:TextField;
      
      public function UI_Register_panel()
      {
         super();
      }
   }
}

