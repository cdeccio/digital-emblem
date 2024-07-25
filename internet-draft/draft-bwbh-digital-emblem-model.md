---
title: Conceptual Model for Digitized Emblems
abbrev: Digital Emblem Models
docname: draft-bwbh-digital-emblem-model-00
category: info

ipr: trust200902

stand_alone: yes
pi: [toc, sortrefs, symrefs]

author:
 -
    name: Bill Woodcock
    ins: B. Woodcock
    org: PCH
    email: woody@pch.net
 -
    name: Brian Haberman
    ins: B. Haberman
    org: Johns Hopkins University
    email: brian@innovationslab.net

normative:
  RFC2119:
  RFC8174:
  I-D.haberman-digital-emblem-ps:

informative:
    
--- abstract

This document describes the conceptual models of use for digial emblems.
--- middle

# Introduction

Digital emblems are intended to be modern counterparts to the visual 
markings which have historically been used to comply with marking 
requirements found in international law. Digital emblems provide 
mechanisms for authentication, access control, dynamic data and 
bidirectional data flows, revocation, non-repudiatability, and the 
inclusion of external data, rich media, and many other benefits which 
are difficult or impossible to convey with a rattle-can and a stencil.

Although there are many different marks, applied by many different 
parties, for many different purposes, the task of marking, per se, is 
simply one of conveying information between parties. As long as a 
protocol is capable of conveying any information parties agree to use 
it for, it succeeds.  If it is too prescriptive, or tries too hard to 
anticipate and circumscribe uses, it fails.

Many use-cases for digital counterparts to physical markings have been 
documented [I-D.haberman-digital-emblem-ps]. This document distills 
the common technological requirements of those use-cases into a single 
harmonized set of requirements; the superset of requirements which are 
common to multiple intergovernmental organizations and multiple bodies 
of international law. From this set of common requirements is derived 
a conceptual models of digital emblems.

## Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted
as described in BCP 14 {{RFC2119}}{{RFC8174}} when, and only when, they appear in all capitals,
as shown here.

# Digital Emblems Roles & Relationships

An issuer creates digital emblems and cryptographically signs them.

Digital emblems are bound to assets or asset classes by descriptions.

Validators evaluate the digital signature which relates the issuer to the digital emblem, and the
description which binds the digital emblem to the asset, see {{figrel}}.

~~~~~~~~~~

       +--------+
       | Issuer |
       +----+---+
            |
  Signature |<------------------+
            |                   |
       +----+----+              | +-----------+
       | Digital |   Evaluation +-| Validator |
       | Emblem  |              | +-----------+
       +----+----+              |
            |                   |
Description |<------------------+
            |
        +---+---+
        | Asset |
        +-------+

~~~~~~~~~~
{: #figrel title="Digital Emblem Relationships"}

A distribution mechanism is used by the issuer to communicate the digital emblem to the validator.
This mechanism may be access-controlled, and may require that validators authenticate themselves in
order to gain access to an emblem.  A physical representation of a digital emblem may be used by the
issuer to direct validators to the digital emblem, or to communicate the digital emblem. Thus a
physical representation may be either a non-unique embodiment of the emblem, or it may be a signpost
directing validators to an emblem via a separate distribution mechanism.  It should be understood
neither the physical representation nor the distribution mechanism are the emblem.  The emblem is a
cryptographically signed bundle of data records associated by a common name.

# Digital Emblem Data Model

A digital emblem consists of a bundle of records which identify the issuer, bind the record to the
marked asset, and provide a communications channel from issuer to validator which can be used to convey
Information regarding the asset and its handling which may not be presently anticipated by current
implementors. {{figbind}} illustrates the record bundles for issuers and assets. {{figcomm}} shows the
channels used to convey the information to a validator.

~~~~~~~~~~

    +------------------------+      +----------------------------+
    |         Issuer         |      |           Asset            |
    +------------------------+      +----------------------------+
+===| Visual representation  |======| Temporal scope of validity |===+
||  | Identification of law  |      | Spatial scope of validity  |  ||
||  | Contact information    |      | SI unit of size or weight  |  ||
||  | Handling flags         |      | WCO standard quantity      |  ||
||  | Issuer's signature     |      | ISO 4217 unit of currency  |  ||
||  | Third-party signatures |      | Names and serial numbers   |  ||
||  +------------------------+      | Distinguishing marks       |  ||
||                                  | External references        |  ||
||                                  +----------------------------+  ||
||                                                                  ||
||          Standardized digital emblem data elements               ||
||                                                                  ||
+====================================================================+

~~~~~~~~~~
{: #figbind title="Issuer and Asset Bundles and Binding"}


~~~~~~~~~~

            --- Data at rest ----------------->
+--------+  --- Data in flight --------------->
| Issuer |  --- In-band network response ----->
+--------+  --- Passive RF transponder ------->
            --- Active RF transponder --------> +-----------+
            --- Active RF beacon -------------> | Validator |
            --- Passive optical marking ------> +-----------+
 +-------+  --- Active optical transponder ---> 
 | Asset |  --- Active optical beacon -------->
 +-------+  --- Active audio transponder ----->
            --- Active audio beacon ---------->

~~~~~~~~~~
{: #figcomm title="Communication channels conveying digital emblem data to validators"}

Digital emblem data bundles may be presented as part of an interactive session between issuer and
validator, as for instance in the case that the validator MUST be authenticated in real time, or
may receive variable information.  Digital emblem data bundles may also be presented as static data
or unidirectional data flows, which may facilitate offline validation.  Digital emblems should be
agnostic as to the mode by which they are communicated to validators, but implementors may wish to
consider methods which encompass both interactive and offline validation, transmission of the whole
digital emblem data bundles or redirective links to them, and should prefer, wherever possible, to
implement digital emblems above already-standardized lower-level transmission protocols, without
requiring exceptions or revisions to those protocols to accommodate digital emblem payloads. A number
of the anticipated possible distribution mechanisms are noted in the diagram above.

# Digital Emblem Functional Requirements

## Goals and Non-goals

   - It MUST be possible to bind a digital emblem to a person, place, thing, digital data at rest, digital data in transit, or an online service (collectively referred to as assets).
   - Putting aside any legal or regulatory restrictions, any entity MAY issue a digital emblem under their own authority and imprimatur without the approval or participation of any other party.
   - Non-goal: The binding of assets and emblems will always be fraught, and markings of any kind MAY be replicated outside the control or intention of a their original author. No protocol can limit the actions of people in the physical world, and thus this protocol focuses on improving the communication channel which allows validators to determine the authenticity of the original emblem (not of a physical representation of the emblem) and the information needed to determine the authenticity of the binding.

## Issuance

   - A digital emblem consists of a set of one or more data elements united by a common label.
   - It SHOULD be possible for a single uniquely-named digital emblem to incorporate data elements which are also used in other digital emblems issued by the same issuer, or other digital emblems issued by other issuers.
   - It SHOULD be possible to organize digital emblems in a hierarchical namespace, in which each node of the namespace MAY contain a bundle of records representing a single digital emblem.
   - It MUST be possible for parties controlling portions of the hierarchical namespace to receive delegations of that space from others above them in the hierarchy, and to perform delegations to others who are then by definition below them in the hierarchy.
   - Any hierarchy of cryptographic signatures used to authenticate digital emblems SHOULD be one and the same as the hierarchy of the namespace.
   - Issuers MUST be free to compose digital emblem of the elements which best fit their uses. No element type SHOULD be a required member of the set.
<!---
   - A digital emblem MUST be capable of displaying a visual representation of any physical emblem which it supplements or replaces. This MUST be in scalable vector format. The preferred aspect-ratio is between 1:1 and 2:1, but MUST NOT exceed 3:1 or 1:3.  The emblem MAY be presented in two versions, one for display against a light background, the other for display against a dark background.  The emblem MUST utilize a transparent background, if it is not a contiguous convex rectangle of the same extent as the file. The emblem MAY utilize variable transparency, and implementations which display it MUST support display of variable transparency.  The visual representation MUST be entirely self-contained, and may not contain any external references, such as to Internet-hosted webfonts or linked URLs.  All current embodiments are anticipated to be static visual images, without animation or sound. While it SHOULD generally be possible to include digital emblem elements from other areas of the digital emblem hierarchy, visual representations MAY only be used within their own cone, or cones linked by an outbound intra-organizational Digital Emblem Peer (DEP) signature. For example, the United Nations logotype might be included as a visual representation within any digital embem in any cone which the UN has signed with an intra-organizational DEP, but may not be used within the cone of CopyCatCo.
--->
   - A visual representation SHOULD be included in any digital emblem bundle which the issuer has reason to believe may be viewed by a human. If a visual representation is included it MUST be in scalable vector format.
   - It SHOULD be possible to use a redirection to include-by-reference a bundle of records under a different namespace node, in order to allow for the use of common sets without duplicating them (and keeping them synchronized when updated) to different parts of the hierarchy.  If the redirections contain language codes, this MAY also be a way to allow good localization support without cluttering the top level of the digital emblem.  It could contain these redirectors, for different language-codes, which would expand into the set of records supporting that language.  If someone doesn't speak Turkish, they could ignore all the redirects that were Turkish-language-specific.
   - It SHOULD be possible for an issuer to authenticate potential validators, and respond with different digital emblem data, or no data, depending upon the identity of the validator.
   - It SHOULD be possible for an issuer to specify periods of validity for digital emblems (TTL) and the cryptographic signatures over them, independently of the period of validity of the subject of the digital emblem. For example, it SHOULD be possible to issue a digital emblem which is signed with a key which has a validity period which extends one year into the future and one year in the past, indicating that an asset SHOULD arrive at its destination five days from now, and it SHOULD be possible to mark that digital emblem as cacheable by validators for a period of one day.
   - Issuers SHOULD have the option to make downward delegations within the hierarchical namespace within their control subject to discovery by validators or not subject to discovery, at their option. Upward walking of the hierarchy SHOULD always be available to any validator.

## Validation and Display

   - It SHOULD be possible for a validator and an issuer to conduct a cryptographically private conversation, such that third parties are not able to easily discern what asset the query regards, nor what answer is returned.
<!---
   - Verifier implementations MUST display the visual emblem first, followed by the name of the emblem, followed by a textual description with hyperlinks to the bodies of protective law, followed by the content protected by the emblem.  This ordering MAY be temporal, or spatially top-to-bottom, in the direction of text reading, or front-to-back, in order of preference.  The emblem is not a license, and implementations MUST NOT require user interaction to proceed through these steps, except as MAY normally be needed to "scroll through" or read content.  The emblem SHOULD be distinguished from the content it protects, without requiring any modal interaction on the part of the user.
--->
   - Verifier implementations MUST display the visual representation if it is included in the digital emblem bundle.
   - All text within digital emblems SHOULD be rendered in its native script, and common transliterations MAY also be provided, all identified by ISO 639 language code and Unicode script identifier. The native script version SHOULD always take precedence but validators MAY, at the user’s option, display only appropriate transliterations, if they exist.
   - It SHOULD be possible to determine authoritatively whether a digital emblem is associated with an IP address or ASNs by querying relevant portions of the hierarchical namespace.
   - In the event that a digital emblem does not exist at a node in the hierarchical namespace, it SHOULD be possible to prove that due diligence has been exercised, and that a negative answer was received at a specific time.
   - Offline validation SHOULD be possible, provided a sufficient portion of the digital emblem bundle is present, and all necessary parent signatures/delegations are cached by the validator in then-valid form.
   - As DEP signatures SHOULD be asymmetric, it MAY be desirable to also support discovery of outbound DEP signatures performed from a node in the namespace hierarchy. i.e. to be able to discover what other nodes the current node has provided DEP signatures for.
   - If the digital emblem hierarchical namespace exists within another namespace, sharing a root of trust, it MAY be useful to create a registry which allows the publication of tops of digital emblem cones within the larger namespace, to assist verifiers in locating the authentic tops of the digital emblem namespace cones they’re interested in.
   - Until verification tools are widespread, it MAY be useful to have a backwards-compatible mechanism of displaying digital emblem information in a less-secure context, for instance web browsers which are incapable of verifying digital emblem content might still be capable of displaying it, with an indication that it has not been verified.

## Binding of Issuer to Digital Emblem

   - It MUST be possible to cryptographically verify that the content of a digital emblem is complete and has not been modified.
   - It MUST be possible to cryptographically authenticate the issuing party of a Digital Emblem.
   - At any level of the digital emblem namespace hierarchy, it MUST be possible to use a DEP record to contextualize the issuing party of a Digital Emblem in terms of a "web of trust" consisting of other related organizations, other emblem issuers within the same organization, or other authenticated entities which can "vouch for" the legitimacy of the issuing party in a cross-signing web-of-trust, with the nature of the relationship between the namespace node and the signing entity characterized using a small standardized set of relationship types. These SHOULD include the ability to denote one cone of the hierarchy as functionally identical to another (in the event that two cones within the namespace, neither of which is within the other, are functionally identical or under common control and policy; intra-organizational signatures which indicate that two cones are under common control and vouch for each other, but have different function and policy; and inter-organizational signatures which indicate that the other organization vouches for this one, in the sense of being a known and trusted partner, for instance. Inter-organizational DEP relationships can be used to differentiate intended organizations from typosquatting impersonators. Some potential relationships which might be encoded in a DEP record include: Treaty signatory, P&I recognizer, Organizational parent, Organizational peer, Organizational child, License grantor, Visa / entry grantor, Work-permit grantor, Residence-permit grantor, Employment certifier, Overflight right grantor, Permission to enter territorial waters grantor, Know-Your-Customer data verifier.
   - It MUST be possible to specify the formal name of the TREATY or international law referenced by the marking: "1961 Vienna Convention on Diplomatic Relations” “The Convention on Wetlands” If the treaty or body of law has a commonly-used informal name, that MAY be provided as a second text string. The name SHOULD be provided in the native script of the title of the treaty, and common transliterations MAY also be provided, identified by ISO language labels.
   - It MUST be possible to indicate the canonical URL of a public copy of the treaty or international law referenced by the marking.
   - It MUST be possible to identify the TREATY ORGANIZATION responsible for administering the relevant body of international law.
   - If a specific PROTECTION is being invoked under international law, it MUST be possible to include a brief description of the legal protection being invoked: "Anti-counterfeiting" "Diplomatic courier" "Endangered species transport"  "Fissionable materials transport"
   - It MUST be possible to identify one or more authoritative points of CONTACT of the digital emblem issuer. It SHOULD be possible to include fields such as person or role name, email, phone, and postal address. If multiple CONTACT parties are identified, they SHOULD also be distinguished as to purpose.

## Binding of Digital Emblem to Asset

   - It SHOULD be possible to bind a digital emblem to an online service by FQDN, IPv4 address, IPv6 address, IP/port combination, URL, ASN, or combinations of those.
   - Binding of digital emblems to assets SHOULD be accomplished by using digital emblem elements to describe the asset, assets, or class of assets to which the digital emblem is bound, using parameters appropriate to the type of asset, the context of communication, and the shared understanding of the issuer and the verifier.
   - Common descriptive elements SHOULD be sufficiently standardized such that they can be displayed by most verification terminals, software, or devices.
   - It MUST be possible for a digital emblem to reference arbitrary externally-hosted media via URLs. References to image URLs (i.e. images which do not contain text) do not need language codes.  URLs to, for instance, PDFs of treaty documents, SHOULD contain the language label indicating the language of text included within the PDF document.
   - The framework of descriptive elements SHOULD NOT be so prescriptive as to preclude the communication of arbitrary structured data in formats understood in common by digital emblem issuers and verifiers, but unanticipated by the digital emblem protocol or its authors.
   - It MUST be possible to specify a temporal scope of validity for a Digital Emblem, composed of one or more temporal periods of validity.
   - It MUST be possible to define temporal scopes and periods of validity which are independent of other time periods inherited from other parts of the protocol stack, such as the TTLs or the validity periods of digital signatures used to authenticate the digital emblem.
   - Each temporal period of validity MUST be of non-negative length; that is, for each one, its end time may not precede its start time.
   - Temporal periods of validity MAY be overlapping, and the areas of overlap shall be treated as positive, not negative.
   - It MUST be possible to specify a spatial scope of validity for a Digital Emblem, composed of one or more volumetric regions of validity.
   - Volumetric regions of validity MAY be overlapping, and the areas of overlap shall be treated as positive, not negative.
   - Volumetric regions of validity MUST be convex and not sufficiently complex or unconventional as to startle improvident interpretation code. Principle of least astonishment applies.
   - For reasons of compatibility with other systems, it MUST be possible to denote volumetric regions of validity as either or both of a lat/lon/alt/rad or by locating the vertices of a geometric solid. Both systems MAY be used within the same digital emblem, and geometric solids are presumed to have precedence over lat/lon/alt/rad spheres.
   - It MUST be possible to associate one or more temporal scopes of validity with one or more spatial scopes of validity.
   - It MUST be possible to describe multiple separate and independent sets of temporal/spatial validities within the same digital emblem.
   - When a marked asset is identified as a numbered member of an enumerated set, it SHOULD be possible to convey its individual number as well as the size of the set. i.e. “crate 2 of 5.”
   - It MUST be possible to denote a quantity, currency, weight or measure using customs-recognized standards, in the format of a paired numerical quantity and named unit, followed by an optional numerical precision in the same units. The unit MAY consist of an ISO 4217 currency code, an SI base unit of length or mass ("m" or "kg"), a WCO unit of quantity (m2, m3, l, kWh, u), or one of the following: persons, pouches, vehicles, aircraft, watercraft, spacecraft, ANY. The quantity and precision (each of which MAY be of value 0) MAY possess an optional floating decimal place.  Precision should be understood to be +/- the previous value.  In conjunction with a Digital Emblem, this could be used, depending on context, to connote a number of vehicles traveling together in convoy, a number of persons in a delegation, a number of diplomatic pouches in a shipment, a quantity or valuation of goods being proffered to customs, an area under protection, etc.  Multiple QTY RRs MAY be associated with the same DNS label, but have no defined precedence or order.
   - It MUST be possible to denote a period of validity, using an ISO 8601 P[n]Y[n]M[n]DT[n]H[n]M[n]S duration OR a start AND end date OR date and time in ISO 8601 extended format OR the word ANY.  Each start and end date/time MAY consist of the word ANY or YYYY, YYYYMMDD, or YYYYMMDDThhmmss.sss, but may not be empty.  Each ISO 8601 extended date MAY be represented in its most compact form, independent of the resolution of the other date.  Start is first, end is second.  A duration MUST stand alone and may not be paired with a date.  A date represents the point in time immediately preceding and including the named date, but subsequent to and not including the previous period of the same resolution.
   - It MUST be possible to define the FORM of the instance of the emblem. Is it a physical plaque, a nametag, an RFID transponder, a painted QRcode, a file on digital storage, a badge attached to a shipping crate, text embroidered onto a garment?  Ideally this SHOULD be a reference to a common registry.
   - It MUST be possible to indicate the TYPE of asset to which the digital emblem is bound. Is it a building, a diplomatic courier, a web site, and email server, files on a flash thumb drive, the contents of a shipping crate? Ideally this SHOULD be a reference to a common registry.
   - It MUST be possible to NAME the asset to which the digital emblem is bound using a proper noun name of the thing, if it has one, such as "Richard Smith" or "Amiens Cathedral”. Names SHOULD be rendered in their native script, and common transliterations MAY also be provided, identified by ISO 639 language code and Unicode script identifier.
   - It MUST be possible to state the unique SERIAL number of the thing being protected, if it has one.
   - It MUST be possible to provide a textual DESCRIPTION of identifying characteristics: "A painting of a standing woman in Elizabethan dress, 92cm wide by 188 cm high, in a gold-leaf wooden frame."
   - It MUST be possible to provide a textual DESCRIPTION of uniquely identifying characteristics: "Initials 'RH' scratched into lower right corner" "Two brown birthmarks of 4mm and 3mm above left eyebrow"
   - It SHOULD be possible to indicate in a simple flag if the digital emblem is problematically no longer known to be physically proximate to the asset it marks (i.e. they may have become separated from each other).
   - It SHOULD be possible to indicate in a simple flag if a physical embodiment of the digital embem is problematically no longer in a known location (i.e. it has been stolen / lost / separated from its asset).
   - It SHOULD be possible to indicate in a simple flag if the asset is problematically no longer in a known location (i.e. it has been stolen / kidnapped / lost).
   - It SHOULD be possible to indicate in a simple flag if the asset has had its legal protections violated.  (For instance, a diplomatic pouch has been opened by unauthorized parties.) In a more elaborate form, this could include time and position, if known, and other details about the violation.
   - It SHOULD be possible to indicate if the issuer requests that informational updates regarding the progress or status of the asset be sent to the specified contact.
   - It SHOULD be possible to indicate the preferred treatment of an asset which is outside its spatial or temporal window of certificate validity. (For instance, a diplomatic envoy whose remit is for Argentina from January 1, 2025 through December 31, 2026, but whose digital emblem is scanned in Brazil: should they receive any special status? For instance, a shipment of medical aid which arrives at a customs checkpoint a year late: should it be returned to sender, forwarded onward to its destination, confiscated, destroyed, donated to a good cause?)
   - It SHOULD be possible for properly-authenticated mobile assets, or the physical instantiations of digital emblems affixed to them, to update the location record associated with the digital emblem instance or the asset or both, in real-time or near-real-time, provided a sufficient communications channel back to the issuer exists.

## Distribution Mechanisms

   - Issuers / servers SHOULD attempt to deliver all records associated with a single digital emblem as a bundle or blob or single transaction, rather than requiring validators to make multiple queries or guess what records to ask for within a node of the namespace hierarchy.
   - Issuers / servers MAY wish to include the chain of parent signatures up to the unitary root of trust, within the digital emblem record blob, so as to facilitate offline validation by validators which have only the root signature cached.
   - It SHOULD be possible for issuers to push new and updated digital emblems to relevant verifiers or trusted intermediary caches, when appropriate, with cryptographic authentication of both parties and encrypted transport between them.

# IANA Considerations

This document makes no requests of the IANA.

# Security Considerations

TBD.

# Contributors

Moez Chakchouk arranged and conducted many of the use-case interviews 
with intergovernmental treaty organizations responsible for bodies of 
international law.

# Acknowledgments

