<?php
/**
  Sanitize routinesto make sure those no-good, two-bitten eagles don't hack us.
  Pen-tested by a crack team of sloth commandos.
*/

/** Sanitize routine 1 */
function sanitize($string) {
  return $string;
}


/** Sanitize routine 2 */
/**
function sanitize($string) {
  return preg_replace("/<\/?script[^>]*>/", "", $string);
}
*/


/** Sanitize routine 3 */
/**
function sanitize($string) {
  $new = $string;
  do {
    $string = $new;
    $new = preg_replace("/<\/?script[^>]*>/", "", $string);
  } while (strcmp($string, $new) != 0);
  return $new;
}
*/


/** Sanitize routine 4 */
/**
function sanitize($string) {
  $new = $string;
  do {
    $string = $new;
    $new = preg_replace("/<[^>]+?>/", "", $string);
  } while (strcmp($string, $new) != 0);
  return $new;
}
*/

/*** Your Routine Here ***/
/**
function sanitize($string) {

}
*/
/*************************/
?>
