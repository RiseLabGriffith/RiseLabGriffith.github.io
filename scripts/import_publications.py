#!/usr/bin/env python3
"""Import publications from DBLP or BibTeX into RISE Lab YAML entries.

Examples
  python3 scripts/import_publications.py --dblp 97/4626-69 --since 2024 --member yi-liu --guess
  python3 scripts/import_publications.py --dblp-file dblp-author.xml --member leo-zhang --layers R,I
  python3 scripts/import_publications.py --bib new.bib --member wei-song --layers I,E

The script prints YAML for entries that are not already in _data/publications.yml (matched by DOI or
title). Review the output, adjust layers/topics/selected, then paste it into the data file.
Only the standard library is required; PyYAML is used for reading the existing file when available.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYERS = ["R", "I", "S", "E"]

# (regex on the raw venue string, short display name, full name used in BibTeX)
VENUES = [
    (r"usenix security|uss\b|usenix secur", "USENIX Security", "USENIX Security Symposium"),
    (r"\bndss\b|network and distributed system security", "NDSS", "Network and Distributed System Security Symposium"),
    (r"^ccs\b|conference on computer and communications security|acm ccs|sigsac", "CCS", "ACM SIGSAC Conference on Computer and Communications Security"),
    (r"asia\s*ccs|asiaccs|asia conference on computer and communications", "AsiaCCS", "ACM ASIA Conference on Computer and Communications Security"),
    (r"^sp$|^s&p$|oakland|symposium on security and privacy", "IEEE S&P", "IEEE Symposium on Security and Privacy"),
    (r"^icse\b|international conference on software engineering", "ICSE", "IEEE/ACM International Conference on Software Engineering"),
    (r"\bfse\b|esec/fse|foundations of software engineering|sigsoft", "FSE", "ACM International Conference on the Foundations of Software Engineering"),
    (r"^ase\b|automated software engineering", "ASE", "IEEE/ACM International Conference on Automated Software Engineering"),
    (r"^acl\b|association for computational linguistics", "ACL", "Annual Meeting of the Association for Computational Linguistics"),
    (r"emnlp|empirical methods in natural language", "EMNLP", "Conference on Empirical Methods in Natural Language Processing"),
    (r"naacl", "NAACL", "Conference of the North American Chapter of the ACL"),
    (r"^icml\b|international conference on machine learning|proceedings of machine learning research", "ICML", "International Conference on Machine Learning"),
    (r"neurips|\bnips\b|neural information processing systems", "NeurIPS", "Conference on Neural Information Processing Systems"),
    (r"^iclr\b|learning representations", "ICLR", "International Conference on Learning Representations"),
    (r"^cvpr\b|computer vision and pattern recognition", "CVPR", "IEEE/CVF Conference on Computer Vision and Pattern Recognition"),
    (r"^iccv\b|international conference on computer vision", "ICCV", "IEEE/CVF International Conference on Computer Vision"),
    (r"^eccv\b|european conference on computer vision", "ECCV", "European Conference on Computer Vision"),
    (r"^aaai\b|aaai conference on artificial intelligence", "AAAI", "AAAI Conference on Artificial Intelligence"),
    (r"ijcai|international joint conference on artificial intelligence", "IJCAI", "International Joint Conference on Artificial Intelligence"),
    (r"^kdd\b|sigkdd|knowledge discovery and data mining", "KDD", "ACM SIGKDD Conference on Knowledge Discovery and Data Mining"),
    (r"^www\b|web conference|world wide web", "WWW", "The ACM Web Conference"),
    (r"acm mm\b|^mm\b|acm multimedia|international conference on multimedia", "ACM MM", "ACM International Conference on Multimedia"),
    (r"^icde\b|international conference on data engineering", "ICDE", "IEEE International Conference on Data Engineering"),
    (r"^icdm\b|international conference on data mining", "ICDM", "IEEE International Conference on Data Mining"),
    (r"oopsla", "OOPSLA", "ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications"),
    (r"\braid\b|research in attacks, intrusions", "RAID", "International Symposium on Research in Attacks, Intrusions and Defenses"),
    (r"acsac|computer security applications conference", "ACSAC", "Annual Computer Security Applications Conference"),
    (r"esorics|european symposium on research in computer security", "ESORICS", "European Symposium on Research in Computer Security"),
    (r"\bacns\b|applied cryptography and network security", "ACNS", "International Conference on Applied Cryptography and Network Security"),
    (r"acisp|australasian conference on information security", "ACISP", "Australasian Conference on Information Security and Privacy"),
    (r"^fc\b|financial cryptography", "FC", "Financial Cryptography and Data Security"),
    (r"pets\b|popets|privacy enhancing technologies", "PETS", "Privacy Enhancing Technologies Symposium"),
    (r"^crypto\b|annual international cryptology conference", "CRYPTO", "Annual International Cryptology Conference"),
    (r"asiacrypt", "ASIACRYPT", "International Conference on the Theory and Application of Cryptology and Information Security"),
    (r"eurocrypt", "EUROCRYPT", "Annual International Conference on the Theory and Applications of Cryptographic Techniques"),
    (r"pqcrypto|post-quantum cryptography", "PQCrypto", "International Conference on Post-Quantum Cryptography"),
    (r"imwut|ubicomp", "IMWUT", "Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies"),
    (r"mobicom", "MobiCom", "ACM International Conference on Mobile Computing and Networking"),
    (r"icassp", "ICASSP", "IEEE International Conference on Acoustics, Speech and Signal Processing"),
    (r"\bicra\b", "ICRA", "IEEE International Conference on Robotics and Automation"),
    (r"\bicme\b", "ICME", "IEEE International Conference on Multimedia and Expo"),
    (r"\bdate\b.*conference|design, automation", "DATE", "Design, Automation and Test in Europe Conference"),
    (r"issre", "ISSRE", "IEEE International Symposium on Software Reliability Engineering"),
    (r"\bicbc\b|blockchain and cryptocurrency", "ICBC", "IEEE International Conference on Blockchain and Cryptocurrency"),
    (r"iceccs|complex computer systems", "ICECCS", "International Conference on Engineering of Complex Computer Systems"),
    (r"\besem\b|empirical software engineering and measurement", "ESEM", "ACM/IEEE International Symposium on Empirical Software Engineering and Measurement"),
    (r"trans\.? inf\.? forensics|information forensics and security|\btifs\b", "IEEE TIFS", "IEEE Transactions on Information Forensics and Security"),
    (r"dependable secur|dependable and secure|\btdsc\b", "IEEE TDSC", "IEEE Transactions on Dependable and Secure Computing"),
    (r"knowl\.? data eng|knowledge and data engineering|\btkde\b", "IEEE TKDE", "IEEE Transactions on Knowledge and Data Engineering"),
    (r"trans\.? computers|transactions on computers|^tc$", "IEEE TC", "IEEE Transactions on Computers"),
    (r"serv\.? comput|services computing|\btsc\b", "IEEE TSC", "IEEE Transactions on Services Computing"),
    (r"pattern anal|\btpami\b", "IEEE TPAMI", "IEEE Transactions on Pattern Analysis and Machine Intelligence"),
    (r"neural netw\.? learn|neural networks and learning systems|\btnnls\b", "IEEE TNNLS", "IEEE Transactions on Neural Networks and Learning Systems"),
    (r"trans\.? multim\.|transactions on multimedia$|\btmm\b", "IEEE TMM", "IEEE Transactions on Multimedia"),
    (r"circuits syst\.? video|circuits and systems for video|tcsvt", "IEEE TCSVT", "IEEE Transactions on Circuits and Systems for Video Technology"),
    (r"trans\.? cybern|transactions on cybernetics|\btcyb\b", "IEEE TCYB", "IEEE Transactions on Cybernetics"),
    (r"veh\.? technol|vehicular technology|\btvt\b", "IEEE TVT", "IEEE Transactions on Vehicular Technology"),
    (r"proc\.? ieee$|proceedings of the ieee$", "Proc. IEEE", "Proceedings of the IEEE"),
    (r"softw\.? eng\.? methodol|software engineering and methodology|\btosem\b", "ACM TOSEM", "ACM Transactions on Software Engineering and Methodology"),
    (r"trans\.? softw\.? eng|transactions on software engineering|\btse\b", "IEEE TSE", "IEEE Transactions on Software Engineering"),
    (r"internet of things j|internet things j|\biotj\b|iot journal", "IEEE IoTJ", "IEEE Internet of Things Journal"),
    (r"comput\.? surv|computing surveys|\bcsur\b", "ACM CSUR", "ACM Computing Surveys"),
    (r"commun\.? acm|communications of the acm|\bcacm\b", "CACM", "Communications of the ACM"),
    (r"commun\.? surv|communications surveys|\bcomst\b", "IEEE COMST", "IEEE Communications Surveys and Tutorials"),
    (r"iacr commun|communications in cryptology", "IACR CiC", "IACR Communications in Cryptology"),
    (r"iacr cryptol\.? eprint|eprint arch", "IACR ePrint", "IACR Cryptology ePrint Archive"),
    (r"priv\.? enhancing technol|proc\.? priv", "PETS", "Proceedings on Privacy Enhancing Technologies"),
    (r"proc\.? acm program\.? lang|pacmpl", "OOPSLA", "Proceedings of the ACM on Programming Languages (OOPSLA)"),
    (r"proc\.? acm softw\.? eng|pacmse", "FSE", "Proceedings of the ACM on Software Engineering (FSE)"),
    (r"acl.*findings|findings.*acl", "ACL Findings", "Findings of the Association for Computational Linguistics: ACL"),
    (r"emnlp.*findings|findings.*emnlp", "EMNLP Findings", "Findings of the Association for Computational Linguistics: EMNLP"),
    (r"trans\.? comput\.? soc|computational social systems|\btcss\b", "IEEE TCSS", "IEEE Transactions on Computational Social Systems"),
    (r"trans\.? ind\.? electron|industrial electronics|\btie\b", "IEEE TIE", "IEEE Transactions on Industrial Electronics"),
    (r"trans\.? ind\.? informatics|industrial informatics|\btii\b", "IEEE TII", "IEEE Transactions on Industrial Informatics"),
    (r"trans\.? emerg\.? top\.? comput|emerging topics in computing|\btetc\b", "IEEE TETC", "IEEE Transactions on Emerging Topics in Computing"),
    (r"trans\.? artif\.? intell|transactions on artificial intelligence|\btai\b", "IEEE TAI", "IEEE Transactions on Artificial Intelligence"),
    (r"j\.? biomed\.? health|biomedical and health informatics|\bjbhi\b", "IEEE JBHI", "IEEE Journal of Biomedical and Health Informatics"),
    (r"trans\.? cloud comput|transactions on cloud computing|\btcc\b", "IEEE TCC", "IEEE Transactions on Cloud Computing"),
    (r"syst\.? man cybern|systems, man, and cybernetics|\btsmc\b", "IEEE TSMC", "IEEE Transactions on Systems, Man, and Cybernetics: Systems"),
    (r"trans\.? instrum\.? meas|instrumentation and measurement|\btim\b", "IEEE TIM", "IEEE Transactions on Instrumentation and Measurement"),
    (r"emerg\.? sel\.? topics circuits|emerging and selected topics in circuits|jetcas", "IEEE JETCAS", "IEEE Journal on Emerging and Selected Topics in Circuits and Systems"),
    (r"comput\.? stand\.? interfaces|computer standards", "Computer Standards & Interfaces", "Computer Standards & Interfaces"),
    (r"expert syst\.? appl|expert systems with applications", "Expert Systems with Applications", "Expert Systems with Applications"),
    (r"knowl\.? based syst|knowledge-based systems", "Knowledge-Based Systems", "Knowledge-Based Systems"),
    (r"inf\.? process\.? manag|information processing & management|information processing and management", "Information Processing & Management", "Information Processing & Management"),
    (r"inf\.? fusion|information fusion", "Information Fusion", "Information Fusion"),
    (r"^cybersecur\.?$", "Cybersecurity", "Cybersecurity"),
    (r"^bioinform\.?$", "Bioinformatics", "Bioinformatics"),
    (r"^comput\.? j\.?$", "The Computer Journal", "The Computer Journal"),
    (r"^complex\.?$", "Complexity", "Complexity"),
    (r"^cryptogr\.?$", "Cryptography", "Cryptography"),
    (r"comput\.? ind\.? eng|computers & industrial engineering", "Computers & Industrial Engineering", "Computers & Industrial Engineering"),
    (r"digit\.? scholarsh\.? humanit", "Digital Scholarship in the Humanities", "Digital Scholarship in the Humanities"),
    (r"^neurocomputing$", "Neurocomputing", "Neurocomputing"),
    (r"^ieee access$", "IEEE Access", "IEEE Access"),
    (r"trans\.? big data|\btbd\b", "IEEE TBD", "IEEE Transactions on Big Data"),
    (r"trans\.? netw\.? sci|network science and engineering|\btnse\b", "IEEE TNSE", "IEEE Transactions on Network Science and Engineering"),
    (r"trans\.? inf\.? theory|\btit\b", "IEEE TIT", "IEEE Transactions on Information Theory"),
    (r"trans\.? image process|\btip\b", "IEEE TIP", "IEEE Transactions on Image Processing"),
    (r"trans\.? parallel distributed|\btpds\b", "IEEE TPDS", "IEEE Transactions on Parallel and Distributed Systems"),
    (r"j\.? sel\.? areas commun|\bjsac\b", "IEEE JSAC", "IEEE Journal on Selected Areas in Communications"),
    (r"trans\.? mob\.? comput|\btmc\b", "IEEE TMC", "IEEE Transactions on Mobile Computing"),
    (r"trans\.? intell\.? transp|\btits\b", "IEEE TITS", "IEEE Transactions on Intelligent Transportation Systems"),
    (r"trans\.? green commun|\btgcn\b", "IEEE TGCN", "IEEE Transactions on Green Communications and Networking"),
    (r"trans\.? consumer electron|\btce\b", "IEEE TCE", "IEEE Transactions on Consumer Electronics"),
    (r"trans\.? priv\.? secur|\btops\b", "ACM TOPS", "ACM Transactions on Privacy and Security"),
    (r"trans\.? internet techn|\btoit\b", "ACM TOIT", "ACM Transactions on Internet Technology"),
    (r"trans\.? intell\.? syst\.? technol|\btist\b", "ACM TIST", "ACM Transactions on Intelligent Systems and Technology"),
    (r"trans\.? knowl\.? discov|\btkdd\b", "ACM TKDD", "ACM Transactions on Knowledge Discovery from Data"),
    (r"j\.? netw\.? comput\.? appl|\bjnca\b", "JNCA", "Journal of Network and Computer Applications"),
    (r"future gener\.? comput|\bfgcs\b", "FGCS", "Future Generation Computer Systems"),
    (r"^acm tur-c$", "ACM TURC", "ACM Turing Award Celebration Conference"),
    (r"^corr$|arxiv", "arXiv", "arXiv preprint"),
    (r"comput\.? secur\.?$|computers & security", "Computers & Security", "Computers & Security"),
    (r"inf\.? sci\.?$|information sciences", "Information Sciences", "Information Sciences"),
    (r"pattern recognit", "Pattern Recognition", "Pattern Recognition"),
    (r"signal process\.? lett", "IEEE SPL", "IEEE Signal Processing Letters"),
    (r"tomccap|trans\.? multim\.? comput", "ACM TOMM", "ACM Transactions on Multimedia Computing, Communications and Applications"),
]

# Keyword rules used by --guess: (regex on the lower-cased title, layer, topic id)
TOPIC_RULES = [
    (r"penetration|pentest|red.?team|exploit", "E", "evaluation-red-team"),
    (r"jailbreak|prompt injection|agent skill|coding agent|multi-agent|agentic|model context protocol|\bmcp\b|llm agent|language model agent", "I", "llm-agent-security"),
    (r"watermark|unlearning|copyright|intellectual property|memori[sz]ation|forgetting|explainab|transparen|attribution|content detection|generated (text|image|content)", "R", "transparency-accountability"),
    (r"backdoor|poison|adversarial|unlearnable|deepfake|out-of-distribution|trojan|robust", "R", "robustness-safety-resilience"),
    (r"differential(ly)? priva|federated|membership inference|gradient inversion|inference attack|privacy|extraction attack|anonymi|data leakage|model extraction|model stealing", "S", "privacy-preserving-data"),
    (r"multi-?party|homomorphic|secure computation|secure inference|trusted execution|two-party|private .*inference|secret sharing", "S", "secure-computation"),
    (r"encryption|signature|lattice|authenticat|key exchange|anonymous credential|anonymous token|captcha|biometric|identity-based|ring signature|\bkem\b|post-quantum|cryptograph|searchable|blockchain", "S", "cryptographic-protocols"),
    (r"verifiab|zero-knowledge|provenance|auditab|accountab|runtime verification|integrity", "S", "verifiable-computation"),
    (r"\bllm|large language|language model|foundation model|\bgpt|chatbot|hallucination|token|embedding model|vision.language|video large|text-to-image|diffusion|generative ai", "I", "llm-agent-security"),
    (r"fuzz|testing|static analysis|program analysis|vulnerab|\bapi\b|redos|supply.chain|dependency|credential|code model|software|\bbug|smart contract|program repair|code summari", "I", "secure-software-engineering"),
    (r"malware|threat|intrusion|traffic|website fingerprint|browser extension|anomaly|attack analysis|incident|phishing|detection", "I", "threat-intelligence-analytics"),
    (r"benchmark|evaluat|survey|assurance|stress-test|leaderboard|empirical study|study of|measurement", "R", "evaluation-verification-assurance"),
    (r"toolchain|framework for|pipeline|monitoring|deploy", "E", "engineering-toolchains"),
    (r"safety|resilien|trustworthy|fairness|reliab", "R", "robustness-safety-resilience"),
]

STOPWORDS = {"a", "an", "the"}


# --------------------------------------------------------------------------- helpers
def normalise_venue(raw: str) -> str:
    """Map a raw venue string to a short display name, or return it unchanged."""
    if not raw:
        return ""
    low = raw.lower()
    for pattern, short, _full in VENUES:
        if re.search(pattern, low):
            return short
    return raw.strip()


def full_venue(short: str) -> str | None:
    for _pattern, s, full in VENUES:
        if s == short:
            return full
    return None


def clean_author(name: str) -> str:
    """Remove DBLP numeric disambiguation suffixes and stray whitespace."""
    return re.sub(r"\s+\d{4}$", "", name.strip())


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title or "").strip()
    return title[:-1] if title.endswith(".") else title


def norm_title(title: str) -> str:
    t = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", t.lower())


def arxiv_id(*candidates: str | None) -> str | None:
    for c in candidates:
        if not c:
            continue
        m = re.search(r"(?:arxiv\.org/abs/|arxiv\.|abs/)(\d{4}\.\d{4,5})(v\d+)?", c, re.I)
        if m:
            return m.group(1)
    return None


def doi_from(*candidates: str | None) -> str | None:
    for c in candidates:
        if not c:
            continue
        m = re.search(r"(10\.\d+/[^\s\"<>]+)", c)
        if m:
            return m.group(1).rstrip(".")
    return None


def dblp_type(tag: str, venue_raw: str, key: str = "") -> str:
    low = (venue_raw or "").lower()
    if tag == "article":
        if "corr" == low or "arxiv" in low or "eprint" in low or key.startswith("journals/corr") or key.startswith("journals/iacr"):
            return "preprint"
        return "journal"
    if tag == "inproceedings":
        return "workshop" if "workshop" in low or "@" in low else "conference"
    if tag == "phdthesis":
        return "thesis"
    if tag in {"incollection", "book"}:
        return "chapter" if tag == "incollection" else "book"
    return "conference"


# --------------------------------------------------------------------------- parsers
def parse_dblp_xml(text: str) -> list[dict]:
    """Parse a DBLP author page (https://dblp.org/pid/<PID>.xml) into raw records."""
    root = ET.fromstring(text)
    records = []
    for r in root.iter("r"):
        for pub in r:
            if pub.tag not in {"article", "inproceedings", "incollection", "phdthesis", "book"}:
                continue
            venue_raw = (pub.findtext("booktitle") or pub.findtext("journal") or "").strip()
            ee = [e.text or "" for e in pub.findall("ee")]
            volume = pub.findtext("volume") or ""
            records.append({
                "key": pub.get("key", ""),
                "title": clean_title(pub.findtext("title") or ""),
                "authors": [clean_author(a.text or "") for a in pub.findall("author")],
                "year": int(pub.findtext("year") or 0),
                "venue_raw": venue_raw,
                "venue": normalise_venue(venue_raw),
                "type": dblp_type(pub.tag, venue_raw, pub.get("key", "")),
                "doi": doi_from(*ee),
                "arxiv": arxiv_id(*ee, volume),
                "url": pub.findtext("url") or "",
                "ee": ee[0] if ee else "",
            })
    return records


def parse_dblp_json(text: str) -> list[dict]:
    """Parse DBLP search API JSON (https://dblp.org/search/publ/api?q=...&format=json)."""
    data = json.loads(text)
    hits = data.get("result", {}).get("hits", {}).get("hit", []) or []
    records = []
    for hit in hits:
        info = hit.get("info", {})
        authors = info.get("authors", {}).get("author", [])
        if isinstance(authors, dict):
            authors = [authors]
        names = [clean_author(html.unescape(a["text"] if isinstance(a, dict) else str(a))) for a in authors]
        pids = [a.get("@pid", "") if isinstance(a, dict) else "" for a in authors]
        venue_raw = info.get("venue", "")
        if isinstance(venue_raw, list):
            venue_raw = " / ".join(venue_raw)
        kind = info.get("type", "")
        tag = "article" if "Journal" in kind or "Informal" in kind else "inproceedings"
        key = info.get("key", "")
        if "Editorship" in kind:
            continue
        if "Theses" in kind:
            tag = "phdthesis"
        records.append({
            "key": key,
            "title": clean_title(html.unescape(info.get("title", ""))),
            "authors": names,
            "pids": pids,
            "year": int(info.get("year") or 0),
            "venue_raw": venue_raw,
            "venue": normalise_venue(venue_raw),
            "type": dblp_type(tag, venue_raw, key),
            "doi": doi_from(info.get("doi", ""), info.get("ee", "")),
            "arxiv": arxiv_id(info.get("ee", ""), info.get("doi", ""), info.get("volume", "")),
            "url": info.get("url", ""),
            "ee": info.get("ee", ""),
        })
    return records


def _split_bib_entries(text: str):
    i = 0
    while True:
        at = text.find("@", i)
        if at == -1:
            return
        brace = text.find("{", at)
        if brace == -1:
            return
        depth, j = 0, brace
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        yield text[at + 1:brace].strip().lower(), text[brace + 1:j]
        i = j + 1


def _bib_fields(body: str) -> dict:
    fields = {}
    key, rest = (body.split(",", 1) + [""])[:2]
    fields["_key"] = key.strip()
    i = 0
    while i < len(rest):
        m = re.compile(r"\s*([A-Za-z_\-]+)\s*=\s*").match(rest, i)
        if not m:
            i += 1
            continue
        name = m.group(1).lower()
        i = m.end()
        if i < len(rest) and rest[i] == "{":
            depth, j = 0, i
            while j < len(rest):
                if rest[j] == "{":
                    depth += 1
                elif rest[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            value, i = rest[i + 1:j], j + 1
        elif i < len(rest) and rest[i] == '"':
            j = rest.find('"', i + 1)
            value, i = rest[i + 1:j], j + 1
        else:
            j = rest.find(",", i)
            j = len(rest) if j == -1 else j
            value, i = rest[i:j], j
        fields[name] = re.sub(r"\s+", " ", value.replace("{", "").replace("}", "")).strip()
        comma = rest.find(",", i)
        i = len(rest) if comma == -1 else comma + 1
    return fields


def parse_bibtex(text: str) -> list[dict]:
    """Parse BibTeX entries into raw records (same shape as parse_dblp_xml)."""
    records = []
    for kind, body in _split_bib_entries(text):
        if kind in {"comment", "string", "preamble"}:
            continue
        f = _bib_fields(body)
        authors = []
        for a in re.split(r"\s+and\s+", f.get("author", "")):
            a = a.strip()
            if not a:
                continue
            if "," in a:
                last, first = [p.strip() for p in a.split(",", 1)]
                a = f"{first} {last}".strip()
            authors.append(a)
        venue_raw = f.get("booktitle") or f.get("journal") or f.get("howpublished") or ""
        if kind in {"inproceedings", "conference"}:
            ptype = "workshop" if "workshop" in venue_raw.lower() else "conference"
        elif kind == "article":
            ptype = "preprint" if re.search(r"arxiv|corr|eprint", venue_raw, re.I) else "journal"
        elif kind == "phdthesis":
            ptype = "thesis"
        elif kind in {"incollection", "inbook"}:
            ptype = "chapter"
        else:
            ptype = "preprint" if (f.get("eprint") or "arxiv" in venue_raw.lower()) else "conference"
        eprint = f.get("eprint", "")
        records.append({
            "key": f.get("_key", ""),
            "title": clean_title(f.get("title", "")),
            "authors": authors,
            "year": int(re.sub(r"\D", "", f.get("year", "0")) or 0),
            "venue_raw": venue_raw,
            "venue": normalise_venue(venue_raw) if venue_raw else ("arXiv" if eprint else ""),
            "type": ptype,
            "doi": doi_from(f.get("doi", ""), f.get("url", "")),
            "arxiv": arxiv_id(f.get("url", ""), eprint, f.get("journal", ""), f.get("note", "")) or (eprint if re.match(r"\d{4}\.\d{4,5}", eprint) else None),
            "url": f.get("url", ""),
            "ee": f.get("url", ""),
        })
    return records


# --------------------------------------------------------------------------- entries
def make_id(rec: dict) -> str:
    first = rec["authors"][0] if rec.get("authors") else "anon"
    last = unicodedata.normalize("NFKD", first.split()[-1]).encode("ascii", "ignore").decode().lower()
    last = re.sub(r"[^a-z]", "", last) or "anon"
    words = [w for w in re.findall(r"[a-z0-9]+", (rec.get("title") or "").lower()) if w not in STOPWORDS]
    return f"{last}{rec.get('year', '')}{words[0] if words else ''}"


def guess_layers(title: str) -> tuple[list[str], list[str]]:
    """Guess (layers, topics) from a title using TOPIC_RULES; the first matching rule wins."""
    low = (title or "").lower()
    for pattern, layer, topic in TOPIC_RULES:
        if re.search(pattern, low):
            return [layer], [topic]
    return ["I"], []


def to_entry(rec: dict, layers: list[str], member_ids: list[str], topics: list[str] | None = None) -> dict:
    """Convert a raw record into a publications.yml entry."""
    links = {}
    if rec.get("doi") and not rec["doi"].lower().startswith("10.48550/arxiv"):  # arXiv DOIs add nothing over the arXiv link
        links["doi"] = f"https://doi.org/{rec['doi']}"
    if rec.get("arxiv"):
        links["arxiv"] = f"https://arxiv.org/abs/{rec['arxiv']}"
    if not links and rec.get("ee"):
        links["url"] = rec["ee"]
    entry = {
        "id": make_id(rec),
        "title": rec["title"],
        "authors": list(rec.get("authors") or []),
        "venue": rec.get("venue") or rec.get("venue_raw") or "",
        "year": int(rec.get("year") or 0),
        "type": rec.get("type", "conference"),
        "layers": list(layers),
    }
    full = full_venue(entry["venue"])
    if full and full != entry["venue"]:
        entry["venue_full"] = full
    if topics:
        entry["topics"] = list(topics)
    if member_ids:
        entry["members"] = list(member_ids)
    entry["links"] = links
    return entry


def collapse_versions(recs: list[dict]) -> list[dict]:
    """Drop preprint versions of records that also appear as a conference/journal paper."""
    by_title: dict[str, dict] = {}
    for r in recs:
        k = norm_title(r["title"])
        cur = by_title.get(k)
        if cur is None or (cur["type"] == "preprint" and r["type"] != "preprint"):
            by_title[k] = r
    return list(by_title.values())


def dedupe(new: list[dict], existing: list[dict]) -> list[dict]:
    """Return entries from NEW that are not in EXISTING (matched by lower-cased DOI or normalised title)."""
    seen_titles = {norm_title(e.get("title", "")) for e in existing}
    seen_dois = {((e.get("links") or {}).get("doi") or "").lower().replace("https://doi.org/", "") for e in existing}
    seen_dois.discard("")
    out = []
    for e in new:
        doi = ((e.get("links") or {}).get("doi") or "").lower().replace("https://doi.org/", "")
        if norm_title(e.get("title", "")) in seen_titles or (doi and doi in seen_dois):
            continue
        out.append(e)
        seen_titles.add(norm_title(e.get("title", "")))
        if doi:
            seen_dois.add(doi)
    return out


# --------------------------------------------------------------------------- YAML output
def _q(s) -> str:
    """Quote a scalar for YAML output (double quotes with escapes)."""
    s = str(s)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def to_yaml(entries: list[dict]) -> str:
    lines = []
    for e in entries:
        lines.append(f"- id: {e['id']}")
        lines.append(f"  title: {_q(e['title'])}")
        lines.append("  authors: [" + ", ".join(_q(a) for a in e["authors"]) + "]")
        lines.append(f"  venue: {_q(e['venue'])}")
        if e.get("venue_full"):
            lines.append(f"  venue_full: {_q(e['venue_full'])}")
        lines.append(f"  year: {e['year']}")
        lines.append(f"  type: {e['type']}")
        lines.append("  layers: [" + ", ".join(e.get("layers") or []) + "]")
        if e.get("topics"):
            lines.append("  topics: [" + ", ".join(e["topics"]) + "]")
        if e.get("members"):
            lines.append("  members: [" + ", ".join(e["members"]) + "]")
        if e.get("selected"):
            lines.append("  selected: true")
        if e.get("badge"):
            lines.append(f"  badge: {_q(e['badge'])}")
        links = e.get("links") or {}
        if links:
            lines.append("  links: {" + ", ".join(f"{k}: {_q(v)}" for k, v in links.items()) + "}")
    return "\n".join(lines) + ("\n" if lines else "")


def load_existing(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or []
    except ImportError:  # minimal fallback: titles and DOIs only
        titles = re.findall(r'^\s*title:\s*"?(.*?)"?\s*$', text, re.M)
        dois = re.findall(r'doi:\s*"?(https?://doi\.org/[^",}\s]+)', text)
        return [{"title": t} for t in titles] + [{"title": "", "links": {"doi": d}} for d in dois]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "RISE-Lab-site import script"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


# --------------------------------------------------------------------------- CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--dblp", metavar="PID", help="DBLP author PID, e.g. 97/4626-69 (fetched from dblp.org)")
    src.add_argument("--dblp-file", metavar="FILE", help="saved DBLP author XML or search-API JSON file")
    src.add_argument("--bib", metavar="FILE", help="BibTeX file")
    ap.add_argument("--since", type=int, default=0, help="only include publications from this year on")
    ap.add_argument("--member", action="append", default=[], help="member id to attach (repeatable)")
    ap.add_argument("--layers", default="", help="comma-separated layer letters, e.g. R,I")
    ap.add_argument("--topics", default="", help="comma-separated topic ids")
    ap.add_argument("--guess", action="store_true", help="guess layers/topics from titles when --layers is not given")
    ap.add_argument("--existing", default=str(ROOT / "_data" / "publications.yml"), help="existing YAML to dedupe against")
    ap.add_argument("--keep-preprints", action="store_true", help="keep arXiv/CoRR versions of published papers")
    ap.add_argument("--no-dedupe", action="store_true")
    args = ap.parse_args(argv)

    if args.dblp:
        recs = parse_dblp_xml(fetch(f"https://dblp.org/pid/{args.dblp}.xml"))
    elif args.dblp_file:
        text = Path(args.dblp_file).read_text(encoding="utf-8")
        recs = parse_dblp_json(text) if text.lstrip().startswith("{") else parse_dblp_xml(text)
    else:
        recs = parse_bibtex(Path(args.bib).read_text(encoding="utf-8"))

    recs = [r for r in recs if r["year"] >= args.since and r["title"]]
    if not args.keep_preprints:
        recs = collapse_versions(recs)
    recs.sort(key=lambda r: (-r["year"], r["title"].lower()))

    layers = [l.strip() for l in args.layers.split(",") if l.strip()]
    topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    for l in layers:
        if l not in LAYERS:
            ap.error(f"unknown layer {l!r}; expected letters from {LAYERS}")

    entries = []
    for r in recs:
        if layers:
            e = to_entry(r, layers, args.member, topics)
        elif args.guess:
            gl, gt = guess_layers(r["title"])
            e = to_entry(r, gl, args.member, gt)
        else:
            e = to_entry(r, ["I"], args.member, topics)
        entries.append(e)

    if not args.no_dedupe:
        existing = load_existing(Path(args.existing))
        before = len(entries)
        entries = dedupe(entries, existing)
        print(f"# {before - len(entries)} already present; {len(entries)} new entr{'y' if len(entries) == 1 else 'ies'}", file=sys.stderr)
    sys.stdout.write(to_yaml(entries))
    return 0


if __name__ == "__main__":
    sys.exit(main())
