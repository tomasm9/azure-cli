.. :changelog:

Release History
===============
0.3.6
+++++
* Minor fixes.

0.3.5
+++++
* namespace: Added network-rule commands.
* namespace create/update: Added --default-action argument for network rules.

0.3.4
+++++
* eventhubs eventhub create/update: Added --skip-empty-archives flag to support empty archives in capture.

0.3.3
+++++
* Minor fixes

0.3.2
+++++
* Minor fixes

0.3.1
+++++
* eventhubs namespace create/update: Added --enable-kafka flag to support Kafka.

0.3.0
+++++
* Fix eventhub update command
* BREAKING CHANGE: 'list' commands errors for resource(s) NotFound(404) are now handled in the typical way instead of showing empty list

0.2.4
+++++
* Minor fixes

0.2.3
+++++
* Minor fixes

0.2.2
+++++
* added readonly property 'pendingReplicationOperationsCount' to georecovery-alias

0.2.1
+++++
* updated help for the parameter --partition-count of eventhub

0.2.0
+++++
* BREAKING CHANGE: 'show' commands log error message and fail with exit code of 3 upon a missing resource.

0.1.4
++++++
* Minor fixes.

0.1.3
+++++
* Minor fixes

0.1.2
++++++
* Fix package wheel
* `sdist` is now compatible with wheel 0.31.0

0.1.1
+++++
* Suppress the eventhubs extension from being loaded now.

0.1.0
+++++
* Initial release.

