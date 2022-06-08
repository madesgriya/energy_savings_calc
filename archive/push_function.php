<?php
add_action( 'wpforms_process_complete', 'sendingDataToLambda', 10, 4 );

  function sendingDataToLambda( $fields, $entry, $form_data, $entry_id) {

    //Specify WPForm ID you have there

    //if form ID is 1
    if (form_data[id] == 3364) { //add the WPForm ID

      $api_url = 'https://rv28h465sc.execute-api.ap-southeast-1.amazonaws.com/default/energySavingsWebApp'; 
      $body = array(
        'name'                  => $fields['1']['value'],
        'email'                 => $fields['2']['value'],
        'company'               => $fields['3']['value'],
        'facility'              => $fields['4']['value'],
        'buildingSize'          => $fields['7']['value'],
        'curSP'                 => $fields['8']['value'],
        'humidity'              => $fields['9']['value'],
        'desiredSP'             => $fields['10']['value'],
      );
      $request = wp_remote_post( $api_url, array( 'body' => $body ) );

     }
}