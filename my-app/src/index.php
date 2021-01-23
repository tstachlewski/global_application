<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Simple PHP App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="assets/css/bootstrap.min.css" rel="stylesheet">
        <style>body {margin-top: 40px; background-color: #333;}</style>
        <link href="assets/css/bootstrap-responsive.min.css" rel="stylesheet">
        <script src="https://sdk.amazonaws.com/js/aws-sdk-2.4.7.min.js"></script>

    </head>

    <body>
        <div class="container">
            <div class="hero-unit">



                <?php

                $bucket="summit-underthecloud-16";

                $metadata_uri = getenv('ECS_CONTAINER_METADATA_URI');
                $metadata = file_get_contents($metadata_uri . '/task');
                $obj = json_decode($metadata);
                $cluster = $obj->{'Cluster'};

                if (strpos($cluster,"eu-") !== false) {
                    $flag = "https://tomash.s3-eu-west-1.amazonaws.com/eu-flag.png";
                    $color = "0402a9";
                    $suffix = "-europe";
                    $region = "eu-west-1";
                    $cognito = "eu-west-1:19e95849-9b14-47e6-93d0-7c8e8835d350";

                } else {
                    $flag = "https://tomash.s3-eu-west-1.amazonaws.com/us-flag.png";
                    $color = "c30000";
                    $suffix = "-usa";
                    $region = "us-west-1";
                    $cognito = "us-west-1:f3df216e-ec03-4b56-bc56-62335ee35880";
                }

                ?>


        <img src="<?php echo $flag; ?>" align="center" width="150">
        <center>
        <h2>GLOBAL CARTOON THEMES</h2>

        <table>
            <tr>
                <td><video height="240" controls><source src="<?php echo "https://" . $bucket . $suffix . ".s3-" . $region . ".amazonaws.com/01.mp4"; ?>"</video></br>A<img src="https://tomash.s3-eu-west-1.amazonaws.com/like.png">B</td>
                <td><video height="240" controls><source src="<?php echo "https://" . $bucket . $suffix . ".s3-" . $region . ".amazonaws.com/02.mp4"; ?>"</video></br>A<img src="https://tomash.s3-eu-west-1.amazonaws.com/like.png">B</td>
                <td><video height="240" controls><source src="<?php echo "https://" . $bucket . $suffix . ".s3-" . $region . ".amazonaws.com/03.mp4"; ?>"</video></br><img src="https://tomash.s3-eu-west-1.amazonaws.com/like.png"/></td>
            </tr>
            <tr>
                <td><img src="https://tomash.s3-eu-west-1.amazonaws.com/like.png" width="40" onclick="like('1',1);" ><h7 id="likes1">--</h7></td>
                <td><img src="https://tomash.s3-eu-west-1.amazonaws.com/like.png" width="40" onclick="like('2',1);" ><h7 id="likes2">--</h7></td>
                <td><img src="https://tomash.s3-eu-west-1.amazonaws.com/like.png" width="40" onclick="like('3',1);" ><h7 id="likes3">--</h7></td>
            </tr>
        </table>

        </center>


            </div>
        </div>

<script>


     AWS.config.region = "<?php echo $region; ?>" // Region
      AWS.config.credentials = new AWS.CognitoIdentityCredentials({
          IdentityPoolId: "<?php echo $cognito; ?>"
      });


like('1',0);
like('2',0);
like('3',0);

function like(id, inc) {


 var docClient = new AWS.DynamoDB.DocumentClient();

var params = {
      TableName:'likes',
      Key:{
          "movie": id
      },
      UpdateExpression: "set likes = likes + :val",
      ExpressionAttributeValues:{
          ":val": inc
      },
      ReturnValues:"UPDATED_NEW"
  };

  docClient.update(params, function(err, data) {
      if (err) {
          console.log(err);
      } else {
          document.getElementById('likes' + id).innerHTML = data.Attributes["likes"];
      }
  });

}
</script>


        <script src="assets/js/bootstrap.min.js"></script>

        <?php echo '<script type="text/javascript">document.body.style.background = "#' . $color . '" </script>';  ?>

    </body>

</html>
