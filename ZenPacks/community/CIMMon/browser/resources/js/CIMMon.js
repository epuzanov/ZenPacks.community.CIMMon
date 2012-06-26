/*
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
*/

(function(){

var ZC = Ext.ns('Zenoss.component');

function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.CIM_PhysicalMemoryPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CIM_PhysicalMemory',
            autoExpandColumn: 'product',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'size'},
                {name: 'locking'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Slot')
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'size',
                dataIndex: 'size',
                header: _t('Size'),
                width: 70
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.CIM_PhysicalMemoryPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CIM_PhysicalMemoryPanel', ZC.CIM_PhysicalMemoryPanel);
ZC.registerName('CIM_PhysicalMemory', _t('Memory Module'), _t('Memory Modules'));

ZC.CIM_DiskDrivePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CIM_DiskDrive',
            autoExpandColumn: 'name',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'chassis'},
                {name: 'bay'},
                {name: 'storagePool'},
                {name: 'diskType'},
                {name: 'rpm'},
                {name: 'size'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'serialNumber'},
                {name: 'locking'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name')
            },{
                id: 'chassis',
                dataIndex: 'chassis',
                header: _t('Chassis'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'bay',
                dataIndex: 'bay',
                header: _t('Bay'),
                sortable: true
            },{
                id: 'storagePool',
                dataIndex: 'storagePool',
                header: _t('Disk Group'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'diskType',
                dataIndex: 'diskType',
                header: _t('Type'),
                width: 70
            },{
                id: 'rpm',
                dataIndex: 'rpm',
                header: _t('RPM'),
                width: 70
            },{
                id: 'size',
                dataIndex: 'size',
                header: _t('Size')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.CIM_DiskDrivePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CIM_DiskDrivePanel', ZC.CIM_DiskDrivePanel);
ZC.registerName('CIM_DiskDrive', _t('Hard Disk'), _t('Hard Disks'));

ZC.CIM_ChassisPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CIM_Chassis',
            autoExpandColumn: 'name',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'locking'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                width: 80,
                sortable: true
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.CIM_ChassisPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CIM_ChassisPanel', ZC.CIM_ChassisPanel);
ZC.registerName('CIM_Chassis', _t('Chassis'), _t('Chassis'));

ZC.CIM_StoragePoolPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CIM_StoragePool',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'usage'},
                {name: 'totalDisks'},
                {name: 'totalBytesString'},
                {name: 'usedBytesString'},
                {name: 'availBytesString'},
                {name: 'capacity'},
                {name: 'locking'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'usage',
                dataIndex: 'usage',
                header: _t('Usage'),
                width: 150
            },{
                id: 'totalDisks',
                dataIndex: 'totalDisks',
                header: _t('Total Disks')
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Total bytes')
            },{
                id: 'usedBytesString',
                dataIndex: 'usedBytesString',
                header: _t('Used bytes')
            },{
                id: 'availBytesString',
                dataIndex: 'availBytesString',
                header: _t('Free bytes')
            },{
                id: 'capacity',
                dataIndex: 'capacity',
                header: _t('Utilization')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.CIM_StoragePoolPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CIM_StoragePoolPanel', ZC.CIM_StoragePoolPanel);
ZC.registerName('CIM_StoragePool', _t('Disk Group'), _t('Disk Groups'));

ZC.CIM_StorageVolumePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CIM_StorageVolume',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'storagePool'},
                {name: 'diskType'},
                {name: 'accessType'},
                {name: 'totalBytesString'},
                {name: 'locking'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'storagePool',
                dataIndex: 'storagePool',
                header: _t('Disk Group'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'diskType',
                dataIndex: 'diskType',
                header: _t('Disk Type')
            },{
                id: 'accessType',
                dataIndex: 'accessType',
                header: _t('Access'),
                width: 120
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Size')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.CIM_StorageVolumePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CIM_StorageVolumePanel', ZC.CIM_StorageVolumePanel);
ZC.registerName('CIM_StorageVolume', _t('Logical Disk'), _t('Logical Disks'));

ZC.CIM_RedundancySetPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CIM_RedundancySet',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'typeOfSet'},
                {name: 'minNumberNeeded'},
                {name: 'membersCount'},
                {name: 'locking'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'typeOfSet',
                dataIndex: 'typeOfSet',
                header: _t('Type'),
                sortable: true
            },{
                id: 'minNumberNeeded',
                dataIndex: 'minNumberNeeded',
                header: _t('Members Minimum'),
                sortable: true
            },{
                id: 'membersCount',
                dataIndex: 'membersCount',
                header: _t('Members Count'),
                sortable: true
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 100
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.CIM_RedundancySetPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CIM_RedundancySetPanel', ZC.CIM_RedundancySetPanel);
ZC.registerName('CIM_RedundancySet', _t('Redundancy Set'), _t('Redundancy Sets'));

ZC.CIM_ReplicationGroupPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CIM_ReplicationGroup',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'locking'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons
            }]
        });
        ZC.CIM_ReplicationGroupPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CIM_ReplicationGroupPanel', ZC.CIM_ReplicationGroupPanel);
ZC.registerName('CIM_ReplicationGroup', _t('Replication Group'), _t('Replication Groups'));

ZC.CIM_ComputerSystemPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CIM_ComputerSystem',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'slot'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'serialNumber'},
                {name: 'uptime'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitored'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'slot',
                dataIndex: 'slot',
                header: _t('Slot'),
                sortable: true
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'serialNumber',
                dataIndex: 'serialNumber',
                header: _t('Serial #'),
                width: 120
            },{
                id: 'uptime',
                dataIndex: 'uptime',
                header: _t('Uptime')
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.CIM_ComputerSystemPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CIM_ComputerSystemPanel', ZC.CIM_ComputerSystemPanel);
ZC.registerName('CIM_ComputerSystem', _t('Controller'), _t('Controllers'));

})();
