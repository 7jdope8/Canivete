const async = require('async');
const helpers = require('../../../helpers/azure');

module.exports = {
    title: 'Open RDP',
    category: 'Network Security Groups',
    description: 'Determine if TCP port 3389 for RDP is open to the public',
    more_info: 'While some ports such as HTTP and HTTPS are required to be open to the public to function properly, more sensitive services such as RDP should be restricted to known IP addresses.',
    link: 'https://docs.microsoft.com/en-us/azure/virtual-network/manage-network-security-group',
    recommended_action: 'For each VM, open the Networking blade and verify that the Inbound Port Rules do not have a rule for RDP with a source equal to Any or Internet',
    apis: ['networkSecurityGroups:listAll'],

    run: function(cache, settings, callback) {
        var results = [];
        var source = {};
        var locations = helpers.locations(settings.govcloud);

        async.each(locations.networkSecurityGroups, function(location, rcb) {

            var networkSecurityGroups = helpers.addSource(
                cache, source, ['networkSecurityGroups', 'listAll', location]
            );

            if (!networkSecurityGroups) return rcb();

            if (networkSecurityGroups.err || !networkSecurityGroups.data) {
                helpers.addResult(results, 3, 'Unable to query for Network Security Groups: ' + helpers.addError(networkSecurityGroups), location);
                return rcb();
            }

            if (!networkSecurityGroups.data.length) {
                helpers.addResult(results, 0, 'No security groups found', location);
                return rcb();
            }
            
            var ports = {

                'TCP': [3389]
            };

            var service = 'RDP';

            helpers.findOpenPorts(networkSecurityGroups.data, ports, service, location, results);

            rcb();
        }, function() {
            callback(null, results, source);
        });
    }
};