"""OPC UA smoke-test dataset — Sprint 25 §25.1."""

from __future__ import annotations


# Synthetic NodeSet2.xml for the AXLE Practice north-plant Line 7
# example. Uses the standard UANodeSet schema namespace.
OPCUA_NODESET_XML = """<?xml version="1.0" encoding="utf-8"?>
<UANodeSet xmlns="http://opcfoundation.org/UA/2011/03/UANodeSet.xsd"
           xmlns:s1="http://example.com/Plant"
           LastModified="2025-06-30T12:00:00.000Z">
  <NamespaceUris>
    <Uri>http://example.com/Plant</Uri>
  </NamespaceUris>
  <UAObject NodeId="ns=2;s=Line7" BrowseName="2:Line7">
    <DisplayName>Line 7</DisplayName>
    <References>
      <Reference ReferenceType="HasTypeDefinition">i=58</Reference>
    </References>
  </UAObject>
  <UAObject NodeId="ns=2;s=Line7.Press4" BrowseName="2:Press4">
    <DisplayName>Press 4</DisplayName>
    <References>
      <Reference ReferenceType="HasComponent" IsForward="false">ns=2;s=Line7</Reference>
    </References>
  </UAObject>
  <UAVariable NodeId="ns=2;s=Line7.Press4.ServoMotor.VibrationRMS"
              BrowseName="2:VibrationRMS" DataType="i=11">
    <DisplayName>Servo Motor Vibration RMS</DisplayName>
    <References>
      <Reference ReferenceType="HasComponent" IsForward="false">ns=2;s=Line7.Press4</Reference>
    </References>
  </UAVariable>
  <UAVariable NodeId="ns=2;s=Line7.Press4.ServoMotor.CurrentDraw"
              BrowseName="2:CurrentDraw" DataType="i=11">
    <DisplayName>Servo Motor Current Draw</DisplayName>
    <References>
      <Reference ReferenceType="HasComponent" IsForward="false">ns=2;s=Line7.Press4</Reference>
    </References>
  </UAVariable>
  <UAVariable NodeId="ns=2;s=Line7.Press4.ServoMotor.Temperature"
              BrowseName="2:Temperature" DataType="i=11">
    <DisplayName>Servo Motor Temperature</DisplayName>
    <References>
      <Reference ReferenceType="HasComponent" IsForward="false">ns=2;s=Line7.Press4</Reference>
    </References>
  </UAVariable>
  <UAVariable NodeId="ns=2;s=Line7.Press4.CycleCounter"
              BrowseName="2:CycleCounter" DataType="i=7">
    <DisplayName>Press Cycle Counter</DisplayName>
    <References>
      <Reference ReferenceType="HasComponent" IsForward="false">ns=2;s=Line7.Press4</Reference>
    </References>
  </UAVariable>
  <UAVariable NodeId="ns=2;s=Line7.QualityCell.RejectCount"
              BrowseName="2:RejectCount" DataType="i=7">
    <DisplayName>Quality Cell Reject Count</DisplayName>
    <References>
      <Reference ReferenceType="HasComponent" IsForward="false">ns=2;s=Line7</Reference>
    </References>
  </UAVariable>
  <UAVariable NodeId="ns=2;s=Line7.MES.JobId"
              BrowseName="2:JobId" DataType="i=12">
    <DisplayName>MES Job ID</DisplayName>
    <References>
      <Reference ReferenceType="HasComponent" IsForward="false">ns=2;s=Line7</Reference>
    </References>
  </UAVariable>
  <UAVariable NodeId="ns=2;s=Line7.OperatorId"
              BrowseName="2:OperatorId" DataType="i=12">
    <DisplayName>Operator Badge</DisplayName>
    <References>
      <Reference ReferenceType="HasComponent" IsForward="false">ns=2;s=Line7</Reference>
    </References>
  </UAVariable>
</UANodeSet>"""


# Synthetic snapshot for the OPCUAStubClient — paired with the NodeSet above.
OPCUA_SNAPSHOT: dict[str, object] = {
    "ns=2;s=Line7.Press4.ServoMotor.VibrationRMS": 4.21,
    "ns=2;s=Line7.Press4.ServoMotor.CurrentDraw":  18.6,
    "ns=2;s=Line7.Press4.ServoMotor.Temperature":  62.3,
    "ns=2;s=Line7.Press4.CycleCounter":            142_318,
    "ns=2;s=Line7.QualityCell.RejectCount":        7,
    "ns=2;s=Line7.MES.JobId":                      "JOB-2025-Q3-08812",
    "ns=2;s=Line7.OperatorId":                     "OP-31415",
}
