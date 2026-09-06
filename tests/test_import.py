import textwrap

from scripts.import_publications import (dedupe, guess_layers, normalise_venue, parse_bibtex, parse_dblp_xml,
                                         to_entry, to_yaml)

XML = '''<dblpperson><r><inproceedings key="conf/uss/Liu26"><author pid="1">Yi Liu 0069</author><author pid="2">Leo Yu Zhang</author><title>Do Not Mention This.</title><year>2026</year><booktitle>USENIX Security Symposium</booktitle><ee>https://doi.org/10.1/x</ee></inproceedings></r>
<r><article key="journals/tifs/Wei25"><author>Jiaheng Wei</author><author>Yanjun Zhang 0002</author><title>Extracting Private Training Data.</title><year>2025</year><journal>IEEE Trans. Inf. Forensics Secur.</journal><volume>20</volume><ee>https://doi.org/10.1109/TIFS.2025.1</ee></article></r>
<r><article key="journals/corr/abs-2601-1"><author>Yi Liu 0069</author><title>Agent Skills in the Wild.</title><year>2026</year><journal>CoRR</journal><volume>abs/2601.10338</volume><ee>https://doi.org/10.48550/arXiv.2601.10338</ee></article></r></dblpperson>'''


def test_parse_dblp_strips_numeric_suffix_and_period():
    recs = parse_dblp_xml(XML)
    assert recs[0]["authors"] == ["Yi Liu", "Leo Yu Zhang"]
    assert recs[0]["title"] == "Do Not Mention This"
    assert recs[0]["year"] == 2026 and recs[0]["type"] == "conference" and recs[0]["venue"] == "USENIX Security"
    assert recs[0]["doi"] == "10.1/x"


def test_parse_dblp_journal_and_preprint_types():
    recs = parse_dblp_xml(XML)
    assert recs[1]["type"] == "journal" and recs[1]["venue"] == "IEEE TIFS"
    assert recs[2]["type"] == "preprint" and recs[2]["venue"] == "arXiv" and recs[2]["arxiv"] == "2601.10338"


def test_venue_normalisation():
    assert normalise_venue("Proceedings of the ACM Web Conference 2024") == "WWW"
    assert normalise_venue("IEEE Symposium on Security and Privacy") == "IEEE S&P"
    assert normalise_venue("Some Unknown Venue") == "Some Unknown Venue"


def test_to_entry_has_required_fields_and_id():
    e = to_entry(parse_dblp_xml(XML)[0], ["I"], ["yi-liu", "leo-zhang"])
    assert e["id"] == "liu2026do" and e["year"] == 2026 and e["type"] == "conference"
    assert e["layers"] == ["I"] and e["members"] == ["yi-liu", "leo-zhang"]
    assert e["links"]["doi"] == "https://doi.org/10.1/x"


def test_dedupe_by_title_case_insensitive_and_doi():
    a = to_entry(parse_dblp_xml(XML)[0], ["I"], ["yi-liu"])
    b = dict(a, id="other", title=a["title"].upper() + ".", links={})
    c = dict(a, id="third", title="Completely different", links={"doi": a["links"]["doi"]})
    d = dict(a, id="fresh", title="Brand new paper", links={})
    assert dedupe([b, c, d], [a]) == [d]


def test_parse_bibtex_basic():
    bib = textwrap.dedent('''
      @inproceedings{deng2024masterkey,
        title = {{MasterKey}: Automated Jailbreak Across Multiple Large Language Model Chatbots},
        author = {Deng, Gelei and Liu, Yi and Li, Yuekang},
        booktitle = {NDSS},
        year = {2024},
        doi = {10.14722/ndss.2024.24188}
      }
    ''')
    recs = parse_bibtex(bib)
    assert recs[0]["title"] == "MasterKey: Automated Jailbreak Across Multiple Large Language Model Chatbots"
    assert recs[0]["authors"] == ["Gelei Deng", "Yi Liu", "Yuekang Li"]
    assert recs[0]["venue"] == "NDSS" and recs[0]["year"] == 2024 and recs[0]["type"] == "conference"


def test_guess_layers_from_keywords():
    assert guess_layers("Prompt injection attacks against LLM agents") == (["I"], ["llm-agent-security"])
    assert guess_layers("Lattice-based threshold blind signature")[0] == ["S"]


def test_yaml_output_round_trips():
    import yaml
    e = to_entry(parse_dblp_xml(XML)[0], ["I"], ["yi-liu"])
    assert yaml.safe_load(to_yaml([e]))[0]["title"] == e["title"]
