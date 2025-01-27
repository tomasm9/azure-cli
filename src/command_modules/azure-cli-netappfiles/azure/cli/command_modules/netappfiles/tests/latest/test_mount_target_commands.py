# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer

POOL_DEFAULT = "--service-level 'Premium' --size 4"
VOLUME_DEFAULT = "--service-level 'Premium' --usage-threshold 100"
LOCATION = "eastus2"

# No tidy up of tests required. The resource group is automatically removed


class AzureNetAppFilesMountTargetServiceScenarioTest(ScenarioTest):
    def setup_vnet(self, rg, vnet_name, subnet_name):
        self.cmd("az network vnet create -n %s --resource-group %s -l %s" % (vnet_name, rg, LOCATION))
        self.cmd("az network vnet subnet create -n %s --vnet-name %s --address-prefixes '10.0.0.0/24' --delegations 'Microsoft.Netapp/volumes' -g %s" % (subnet_name, vnet_name, rg))

    def current_subscription(self):
        subs = self.cmd("az account show").get_output_in_json()
        return subs['id']

    def create_volume(self, account_name, pool_name, volume_name1, rg, tags=None):
        vnet_name = "cli-vnet-lefr-01"
        subnet_name = "cli-subnet-lefr-01"
        creation_token = volume_name1
        tag = "--tags %s" % tags if tags is not None else ""

        self.setup_vnet(rg, vnet_name, subnet_name)
        self.cmd("az netappfiles account create -g %s -a '%s' -l %s" % (rg, account_name, LOCATION)).get_output_in_json()
        self.cmd("az netappfiles pool create -g %s -a %s -p %s -l %s %s %s" % (rg, account_name, pool_name, LOCATION, POOL_DEFAULT, tag)).get_output_in_json()
        volume1 = self.cmd("az netappfiles volume create --resource-group %s --account-name %s --pool-name %s --volume-name %s -l %s %s --creation-token %s --vnet %s --subnet %s %s" % (rg, account_name, pool_name, volume_name1, LOCATION, VOLUME_DEFAULT, creation_token, vnet_name, subnet_name, tag)).get_output_in_json()

        return volume1

    @ResourceGroupPreparer()
    def test_list_mount_targets(self):
        account_name = "cli-acc-lefr-01"
        pool_name = "cli-pool-lefr-01"
        volume_name = "cli-volume-lefr-01"
        self.create_volume(account_name, pool_name, volume_name, '{rg}')

        volume_list = self.cmd("netappfiles list-mount-targets --resource-group {rg} -a %s -p %s -v %s" % (account_name, pool_name, volume_name)).get_output_in_json()
        assert len(volume_list) == 1
