# Korad3005p
Serial communication with Korad3005p for li-ion battery charging with capacity measurement...

# Program Usage:
  +=[Serial Ports]=======[-ox]    +=[Korad OUTPUT]===================[-ox]     +=[Hot Keys]===========[-ox]
  |                          |    |                                      |     |                          |
  |  Port:/dev/ttyACM1       |    |  Vout [V]:03.73      Time:00:00:26   |     |  1..9 - select port      |
  |                          |    |  Iout [A]:0.900                      |     |  s - rescan ports        |
  |                          |    |  Power [W]:3.35                      |     |  ------------------      |
  |  (1):/dev/ttyACM1        |    |  Energy [Wh]:0.02                    |     |  v - set voltage         |
  |                          |    |  Charge [mAh]:6.25                   |     |  i - set current         |
  |                          |    |                                      |     |  o - set I cut off       |
  |                          |    +======================================+     |  ------------------      |
  +==========================+    +=[Korad SETUP]====================[-ox]     |  r - Run KORAD           |
                                  |                                      |     |  t - Stop KORAD          |
                                  |  Vset [V]:04.30                      |     |  ------------------      |
                                  |  Iset [A]:0.900                      |     |  q - exit                |
                                  |  Ioff [A]:0.010                      |     |                          |
                                  +======================================+     +==========================+



 Cmd: