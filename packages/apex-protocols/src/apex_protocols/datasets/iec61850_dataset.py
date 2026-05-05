"""IEC 61850 smoke-test dataset — Sprint 25 §25.2."""

from __future__ import annotations


# Synthetic SCD for the ER Practice substation example. Minimal but
# structurally valid against IEC 61850-6 (SCL XML schema).
IEC61850_SCD_XML = """<?xml version="1.0" encoding="UTF-8"?>
<SCL xmlns="http://www.iec.ch/61850/2003/SCL" version="2007" revision="B">
  <Header id="north-bay-substation" revision="1" toolID="apex-protocols">
    <History>
      <Hitem version="1" revision="1" when="2025-06-30T12:00:00Z"
             who="apex" what="Initial SCD"/>
    </History>
  </Header>
  <IED name="IED1" type="GenericRelay" manufacturer="ACME Relay Co" configVersion="1.0">
    <Services>
      <DynAssociation/>
      <SettingGroups/>
    </Services>
    <AccessPoint name="S1">
      <Server>
        <Authentication/>
        <LDevice inst="CTRL">
          <LN0 lnClass="LLN0" inst="" lnType="LLN0_TYPE">
            <GSEControl name="GOOSEPos1" appID="0x0001"
                        confRev="1" datSet="DS_PosFlt"/>
          </LN0>
          <LN lnClass="LPHD" inst="1" lnType="LPHD_TYPE"/>
          <LN lnClass="XCBR" inst="1" lnType="XCBR_TYPE"/>
          <LN lnClass="XSWI" inst="1" lnType="XSWI_TYPE"/>
        </LDevice>
        <LDevice inst="MEAS">
          <LN0 lnClass="LLN0" inst="" lnType="LLN0_TYPE">
            <SampledValueControl name="MUSV1" appID="0x4000"
                                 confRev="1" datSet="DS_PhsMeas" smpRate="4800"/>
          </LN0>
          <LN lnClass="MMXU" inst="1" lnType="MMXU_TYPE"/>
        </LDevice>
      </Server>
    </AccessPoint>
  </IED>
</SCL>"""


# Synthetic snapshot for the IEC61850StubClient
IEC61850_SNAPSHOT: dict[str, object] = {
    "IED1/CTRL/XCBR1.Pos.stVal":              "closed",
    "IED1/CTRL/XCBR1.OpCnt.stVal":            48,
    "IED1/MEAS/MMXU1.A.phsA.cVal.mag.f":      218.7,
    "IED1/MEAS/MMXU1.A.phsB.cVal.mag.f":      219.1,
    "IED1/MEAS/MMXU1.A.phsC.cVal.mag.f":      217.9,
    "IED1/MEAS/MMXU1.PPV.phsAB.cVal.mag.f":   13_805.0,
    "IED1/MEAS/MMXU1.TotW.mag.f":             4_812.5,
}
