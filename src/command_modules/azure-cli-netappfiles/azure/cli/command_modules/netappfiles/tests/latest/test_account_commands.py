# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer
LOCATION = "eastus2"

# No tidy up of tests required. The resource group is automatically removed


class AzureNetAppFilesAccountServiceScenarioTest(ScenarioTest):
    @ResourceGroupPreparer(name_prefix='cli_tests_rg_')
    def test_create_delete_account(self):
        account_name = self.create_random_name(prefix='cli', length=24)
        tags = 'Tag1=Value1 Tag2=Value2'

        # create and check
        account = self.cmd("az netappfiles account create --resource-group {rg} --account-name '%s' -l %s --tags %s" % (account_name, LOCATION, tags)).get_output_in_json()
        assert account['name'] == account_name
        assert account['tags']['Tag1'] == 'Value1'
        assert account['tags']['Tag2'] == 'Value2'
        # active directory subgroups not tested here - issue with parameters being interpreted as kwargs. Fully tested at command line instead.
        # assert account['active_directories'][0]['username'] == 'aduser'
        # assert account['active_directories'][0]['smbservername'] == 'SMBSERVER'

        account_list = self.cmd("netappfiles account list --resource-group {rg}").get_output_in_json()
        assert len(account_list) > 0

        # delete and recheck
        self.cmd("az netappfiles account delete --resource-group {rg} --account-name '%s'" % account_name)
        account_list = self.cmd("netappfiles account list --resource-group {rg}").get_output_in_json()
        assert len(account_list) == 0

        # and again with short forms and also unquoted
        account = self.cmd("az netappfiles account create -g {rg} -a %s -l %s --tags %s" % (account_name, LOCATION, tags)).get_output_in_json()
        assert account['name'] == account_name
        # note: key case must match
        assert account['activeDirectories'] is None
        account_list = self.cmd("netappfiles account list --resource-group {rg}").get_output_in_json()
        assert len(account_list) > 0

        self.cmd("az netappfiles account delete --resource-group {rg} -a %s" % account_name)
        account_list = self.cmd("netappfiles account list --resource-group {rg}").get_output_in_json()
        assert len(account_list) == 0

    @ResourceGroupPreparer(name_prefix='cli_tests_rg_')
    def test_list_accounts(self):
        accounts = [self.create_random_name(prefix='cli', length=24), self.create_random_name(prefix='cli', length=24)]

        for account_name in accounts:
            self.cmd("az netappfiles account create -g {rg} -a %s -l %s --tags Tag1=Value1" % (account_name, LOCATION)).get_output_in_json()

        account_list = self.cmd("netappfiles account list -g {rg}").get_output_in_json()
        assert len(account_list) == 2

        for account_name in accounts:
            self.cmd("az netappfiles account delete -g {rg} -a %s" % account_name)

        account_list = self.cmd("netappfiles account list --resource-group {rg}").get_output_in_json()
        assert len(account_list) == 0

    @ResourceGroupPreparer(name_prefix='cli_tests_rg_')
    def test_get_account_by_name(self):
        account_name = self.create_random_name(prefix='cli', length=24)
        account = self.cmd("az netappfiles account create -g {rg} -a %s -l %s" % (account_name, LOCATION)).get_output_in_json()
        account = self.cmd("az netappfiles account show --resource-group {rg} -a %s" % account_name).get_output_in_json()
        assert account['name'] == account_name
        account_from_id = self.cmd("az netappfiles account show --ids %s" % account['id']).get_output_in_json()
        assert account_from_id['name'] == account_name

    @ResourceGroupPreparer(name_prefix='cli_tests_rg_')
    def test_set_account(self):
        # only tags are checked here due to complications of active directory in automated test
        account_name = self.create_random_name(prefix='cli', length=24)
        tag = "Tag1=Value1"

        account = self.cmd("az netappfiles account create -g {rg} -a %s -l %s" % (account_name, LOCATION)).get_output_in_json()
        account = self.cmd("az netappfiles account set --resource-group {rg} -a %s -l %s --tags %s" % (account_name, LOCATION, tag)).get_output_in_json()
        assert account['name'] == account_name
        assert account['tags']['Tag1'] == 'Value1'
        assert account['activeDirectories'] is None

    @ResourceGroupPreparer(name_prefix='cli_tests_rg_')
    def test_update_account(self):
        # only tags are checked here due to complications of active directory in automated test
        account_name = self.create_random_name(prefix='cli', length=24)
        tag = "Tag1=Value1"

        account = self.cmd("az netappfiles account create -g {rg} -a %s -l %s" % (account_name, LOCATION)).get_output_in_json()
        account = self.cmd("az netappfiles account update --resource-group {rg} -a %s --tags %s" % (account_name, tag)).get_output_in_json()
        assert account['name'] == account_name
        assert account['tags']['Tag1'] == 'Value1'
        assert account['activeDirectories'] is None
