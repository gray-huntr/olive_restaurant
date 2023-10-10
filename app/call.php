<?php
            try
            {
                //Set the response content type to application/json
                header("Content-Type:application/json");
                $resp = '{"ResultCode":0,"ResultDesc":"Confirmation recieved successfully"}';
                //read incoming request
                
                    // $user_id = $_GET['account'];
                    // $cat_id = $_GET['cat_id'];
                    // $package = $_GET['package'];
                    // $section = $_GET['section'];
                    
                    $callbackJSONData=file_get_contents('php://input');
                    $callbackData=json_decode($callbackJSONData);
                    $resultCode=$callbackData->Body->stkCallback->ResultCode;
                    // $resultDesc=$callbackData->Body->stkCallback->ResultDesc;
                    // $merchantRequestID=$callbackData->Body->stkCallback->MerchantRequestID;
                    // $checkoutRequestID=$callbackData->Body->stkCallback->CheckoutRequestID;
                    
                    if( $resultCode==0){
                    $amount=$callbackData->Body->stkCallback->CallbackMetadata->Item[0]->Value;
                    $mpesaReceiptNumber=$callbackData->Body->stkCallback->CallbackMetadata->Item[1]->Value;
                    //$b2CUtilityAccountAvailableFunds=$callbackData->Body->stkCallback->CallbackMetadata->Item[3]->Value;
                    $phoneNumber =$callbackData->Body->stkCallback->CallbackMetadata->Item[4]->Value;
                  
                    
                    $servername = "localhost";
                    $username = "root";
                    $password = "";
                    $dbname = "olive_garden";
                    
                                      
                    // Create connection
                    $conn = mysqli_connect($servername, $username, $password, $dbname);
                    // Check connection
                    if (!$conn) {
                      die("Connection failed: " . mysqli_connect_error());
                    }
                    
                    $sql = "INSERT INTO `transactions`(`mpesa_code`, `phone_number`,`amount`)
                    VALUES ('$mpesaReceiptNumber','$phoneNumber','$amount')";
                    
                    if (mysqli_query($conn, $sql)) {
                      echo "New record created successfully";
                    } else {
                      echo "Error: " . $sql . "<br>" . mysqli_error($conn);
                    }
            
                 
                    }//end if
                    
                    else {
                     //reject   
                    }
                 
                 
            } catch (Exception $ex){
                //append exception to errorLog
                $logErr = fopen($errorLog,"a");
                fwrite($logErr, $ex->getMessage());
                fwrite($logErr,"\r\n");
                fclose($logErr);
            }
                //echo response
                echo $resp;
     
        
?>