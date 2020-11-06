#!/usr/bin/env python3 -tt
import urllib.request, ssl, argparse, subprocess, re, time, sys
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Show progress", action='store_const', const=True, default=False)
args = parser.parse_args()
verbose = args.verbose

def main():
    def doCollect(eachid):
        urlrequest = str(BeautifulSoup(urllib.request.urlopen("https://attack.mitre.org/techniques/{}/".format(eachid)).read(),"html.parser").find_all())
        regex = re.compile(r"href=\"\/techniques\/"+str(eachid.replace(".","/"))+r"\/\">[\S\s]\s+[A-Za-z\.\/][\w\-\ \.\/\(\)]+[A-Za-z\(\)]")
        name = re.sub(r"[\S\s]+\s{2,}", r"<span class=\"h5 card-title\">Technique: ", str(re.findall(regex, urlrequest)[0]))
        description = str("<span class=\"h5 card-title\">Description: "+str(re.sub(r"</p><p>", r" ", str(re.sub(r"\<span\s.*\<\/span>", r"", str(re.findall(r"<div class=\"description-body\">[\S\s]{4}(.*)</p>", urlrequest)[1]))).replace(". .",".").replace(".\".",".").replace("<code>","").replace("</code>",""))))+".."
        techniquecard, cards = str(name+description+str(urlrequest.replace("\\n","\n").replace("\n","\\n").split("<div class=\"col-md-4\">\\n<div class=\"card\">\\n<div class=\"card-body\">\\n<div class=\"card-data\" id=\"card-id\">")[1]).split("</div>\\n</div>\\n</div>\\n<div class=\"text-center pt-2 version-button live\">\\n<div class=\"live\">")[0]).replace("\\\"","\""), []
        if ">Detection</h2>" in urlrequest:
            techniquecard = "{}<span Detection: {},".format(techniquecard, re.sub(r">\w+</h3>", r"", str(str(re.sub(r"<a href=\"https://attack.mitre.org/tactics/TA\d{4}\">", r"", str(re.sub(r"([A-Za-z]\.)([A-Z])", r"\1 \2", str(re.sub(r"<a href=\"/software/S\d{4}\">", r"", str(re.sub(r"\[\d+\]", r"", str(re.sub(r"\<sup>[^\>]+\>", r"", str(re.sub(r"\<span[^\>]+\>", r"", str(re.sub(r"<a href=\"/techniques/T\d{4}\">", r"", str(re.sub(r"<a href=\"/techniques/T\d{4}/\d{3}\">", r"", str(str(urlrequest.split(">Detection</h2>")[1].split("<h2 class")[0]).replace("\n","\\n")[12:-14].replace("<code>","").replace("</code>","").replace(",",";").replace(" / ","/").replace("&gt;",">").replace("&lt;","<").replace("&amp;","&").replace("<p>","").replace("</p>","").replace("<ul><li>","(*)").replace("</li><li>","(*)").replace("</li></ul>","(*)").replace("</a>","").replace("\\s ","'s").replace("(*)"," (*)").replace("  "," ").replace("Äô","").replace("Äî","").replace("<em>","").replace("</em>","").replace("</username>","").replace("<labelname> ","").replace("</labelname>","").replace("</sup>","").replace("</span>","")))))))))))))))))).replace(" ; ","; ").replace("\\\\","\\").split("<div class")[0]).replace("  ","").replace("</pid>","").strip("\"")))
        else:
            pass
        if "mitigations/M" in urlrequest:
            techniquecard = techniquecard+"<span Mitigations: "
            try:
                for line in str(str(BeautifulSoup(urllib.request.urlopen("https://attack.mitre.org/techniques/{}/".format(eachid)).read(),"html.parser").find_all("table"))[1:-1]).split("\n"):
                    if line.startswith("<a href=\"/mitigations/M"):
                        techniquecard = "{}{}".format(techniquecard, str(re.sub(r"<a href=\"/mitigations/M\d{4}\"> ", r"", line[0:-5]))+",")
                    else:
                        pass
            except:
                pass
        else:
            pass
        if "software/S" in urlrequest:
            techniquecard = techniquecard+"<span Software: "
            try:
                for line in str(str(BeautifulSoup(urllib.request.urlopen("https://attack.mitre.org/techniques/{}/".format(eachid)).read(),"html.parser").find_all("table"))[1:-1]).split("\n"):
                    if line.startswith("<a href=\"/software/S"):
                        techniquecard = "{}{}".format(techniquecard, str(re.sub(r"<a href=\"/software/S\d{4}\"> ", r"", line[0:-5]))+",")
                    else:
                        pass
            except:
                pass
        else:
            pass
        try:
            for line in str(str(str(BeautifulSoup(urllib.request.urlopen("https://attack.mitre.org/techniques/{}/".format(eachid)).read(),"html.parser").find_all("table"))[1:-1]).split("</tbody>")[1]).split("\n"):
                if line.startswith("<a href=\"/groups/G"):
                    threat_actor_list.append(re.sub(r"<a href=\"/groups/G\d{4}\"> ", r"", line[0:-5]))
                else:
                    pass
        except:
            pass
        for eachcard in techniquecard.replace("Tactics","Tactic").replace("  ","").replace("class=\"h5 card-title\">","").replace("</span>","").replace("\\n<div class=\"card-","").replace("\\n<!--start-indexing-for-search-->","").replace("\\n<!--stop-indexing-for-search-->","").replace("</div>data\" id=\"card-","").replace("</div>data\">","").replace("id\">","").replace("</a>\\ntactics\">","").replace("platforms\">","").replace("</div>","").replace("\\n"," ").replace(", ",",").split("<span ")[1:]:
            cards.append(eachcard.strip(","))
        collectedtechniques.append(str(str(re.sub(r"T\d{4}\">(T\d{4}\')", r"\1", str(cards).replace("\\xa0"," ").replace(" <a href=\"/techniques/","")[1:-1])))+"||||"+str(threat_actor_list))
    subprocess.Popen(["clear"])
    time.sleep(2)
    if verbose:
        print("\n\n   -> Collecting MITRE ATT&CK techniques...\n")
    else:
        pass
    ssl._create_default_https_context = ssl._create_unverified_context
    nooftechniques, counter = re.findall(r"<h6>Sub-techniques: (\d+)</h6>", str(BeautifulSoup(urllib.request.urlopen("https://attack.mitre.org/techniques/enterprise/").read(),"html.parser")))[0], 1
    techniquestable, entries = str(BeautifulSoup(urllib.request.urlopen("https://attack.mitre.org/techniques/enterprise/").read(),"html.parser").find_all("table"))[1:-1], {}
    for techniques in techniquestable.split("<tr class=\"technique\">")[1:]:
        name, mitreid, subtechniques, collectedtechniques, threat_actor_list = str(str(re.sub(r"(/techniques/T|/software/S|/mitigations/M)\d+\">( )", r"\1", str(re.sub(r"<code>([^\<]+)</code>", r"\1", (techniques.replace("<td>\n</td>","<td></td>").replace("<td></td>","").replace("\n<td>","").replace("</td>","").replace("</tr>","").replace("                            ","").replace("                        ","").replace("                    ","").replace(". . ",". ").replace(" </a>","<a href=\"").replace("\n<td colspan=\"2\">","").replace("\n","").replace("<a href=\"<a href=\"","<a href=\"")))).split("<a href=\"")[2]))).strip(), str(str(re.sub(r"/techniques/T\d+\">( )", r"\1", str(re.sub(r"<code>([^\<]+)</code>", r"\1", (techniques.replace("<td>\n</td>","<td></td>").replace("<td></td>","").replace("\n<td>","").replace("</td>","").replace("</tr>","").replace("                            ","").replace("                        ","").replace("                    ","").replace(". . ",". ").replace(" </a>","<a href=\"").replace("\n<td colspan=\"2\">","").replace("\n","").replace("<a href=\"<a href=\"","<a href=\"")))).split("<a href=\"")[1]))).strip(), str(re.sub(r"<code>([^\<]+)</code>", r"\1", (techniques.replace("<td>\n</td>","<td></td>").replace("<td></td>","").replace("\n<td>","").replace("</td>","").replace("</tr>","").replace("                            ","").replace("                        ","").replace("                    ","").replace(". . ",". ").replace(" </a>","<a href=\"").replace("\n<td colspan=\"2\">","").replace("\n","").replace("<a href=\"<a href=\"","<a href=\"")))), [], []
        doCollect(mitreid)
        progress = str(round(round(int(counter)/int(nooftechniques)*100, 2)*2, 2))
        if verbose:
            if progress.startswith("10.3") or progress.startswith("20.1") or progress.startswith("30.4") or progress.startswith("40.2") or progress.startswith("50.5") or progress.startswith("60.3") or progress.startswith("70.1") or progress.startswith("80.4") or progress.startswith("90.2"):
                print("     -> Progress: {}% complete...".format(progress))
            else:
                pass
            counter += 1
        else:
            pass
        for eachsub in subtechniques.split("<a href=\"")[4:]:
            subid = str(re.sub(r"/techniques/T\d+/\d+\">( )", r"\1", str(eachsub.replace("<tr class=\"sub technique\">","").strip()))).strip()
            if subid.startswith(".0"):
                doCollect(str(mitreid)+"/"+str(subid.strip(".")))
            else:
                pass    
            for eachtechnique in collectedtechniques:
                for eachtactic in str(eachtechnique.split("'Tactic: ")[1]).split("'")[0].split(","):
                    for eachplatform in str(eachtechnique.split("'Platforms: ")[1]).split("'")[0].split(","):
                        key, value = str(re.sub(r"(CAPEC ID: )<a href=\"https://capec.mitre.org/data/definitions/\d+.html\" target=\"_blank\">(CAPEC-\d+)</a> ,", r"\1\2", str(eachtechnique.split(", 'Tactic: ")[0]+", 'Tactic: "+eachtactic+"', 'Platforms: "+eachplatform+", "+str(str(eachtechnique.split("'Platforms: ")[1]).split("'")[1:]).replace("', ', ', '",", ").replace("', ', ","").replace("', '","")[1:-3]).replace("'",""))).split("||||")
                        entries[key] = value
    if verbose:
        print("\n   -> Collection of MITRE ATT&CK Techniques completed.\n\n")
    else:
        pass
    with open("collectedMITRE.csv", "a") as mitrecsv:
        mitrecsv.write("name,description,subid,id,tactic,platform,system_requirements,permissions_required,effective_permissions,data_sources,defense_bypassed,version,created,last_modified,detection,mitigations,software,threat_actor\n")
        for k, v in entries.items():
            details = str(str(re.sub(r"T\d{4}/\d{3}\">T\d{4}\.\d{3}</a>", r"", re.sub(r"T\d{4}\.\d{3}</a>,<a href=\"/techniques/T\d{4}/\d{3}\">", r"", k))).replace(" tactics\">","").replace(", Sub-techniques: , ",", ").replace(", Sub-techniques:  No sub-techniques, ",", ").replace(", ","<>").replace(",",";").replace("<>",",").replace("\\\\u202f"," "))
            for eachvalue in str(str(v).replace("\\'","'").replace("[","").replace("]","").strip()).split(", "):
                name = re.findall(r"^Technique: ([^\,]+)\,", details)[0]
                description = str(str(re.sub(r"([a-z]\.)([A-Z])", r"\1 \2", str(str(re.sub(r"<a href=\"https://attack\.mitre\.org/tactics/TA\d{4}\">", r"", str(re.sub(r"<a href=\"/software/S\d{4}\">", r"", str(re.sub(r"T[\d\.\/]{4,8}\">", r" ", str(re.findall(r"Description: ([\S\s]+)\.\.\,", details.replace(". ..","..").replace("...","..").replace(". ,",".,").replace(".\",",".,").replace("&gt;",">").replace("&lt;","<").replace("<p>","").replace("</p>","").replace("<ul><li>","(*)").replace("</li><li>","(*)").replace("</li></ul>","(*)").replace("</a>","").replace("\\s ","'s").replace("(*)"," (*)").replace("  "," ").replace("Äô","").replace("Äî","").replace("<em>","").replace("</em>","").replace("</username>","").replace("<labelname> ","").replace("</labelname>",""))[0]))))))).replace(";","; ").replace(" / ","/").replace("<a href=\"/techniques/","")))).strip(":")+".").replace("..",".").replace("tokens.may","tokens may").replace("\\\\","\\")
                techniqueid = re.findall(r"ID: (T[^\,]+)\,", details)[0]
                if "." in techniqueid:
                    row = "{},{},{}".format(name, description, techniqueid)
                else:
                    row = "{},{},{}.000".format(name, description, techniqueid)
                if "Sub-technique of:" in details:
                    row = "{},{}".format(row, str(re.findall(r"Sub-technique of: (T[^\,]+)\,", details)[0]))
                else:
                    row = "{},{}".format(row, re.findall(r"ID: (T[^\,]+)\,", details)[0])
                row = "{},{}".format(row, re.findall(r"Tactic: ([^\,]+)\,", details)[0])
                row = "{},{}".format(row, re.findall(r"Platforms: ([^\,]+)\,", details)[0])
                if "System Requirements:" in details:
                    row = "{},{}".format(row, str(re.findall(r"System Requirements: ([^\,]+)\,", details)[0]).replace("<code>","").replace("</code>",""))
                else:
                    row = "{},-".format(row)
                if "Permissions Required:" in details:
                    row = "{},{}".format(row, str(re.findall(r"Permissions Required: ([^\,]+)\,", details)[0]))
                else:
                    row = "{},-".format(row)
                if "Effective Permissions:" in details:
                    row = "{},{}".format(row, str(re.findall(r"Effective Permissions: ([^\,]+)\,", details)[0]))
                else:
                    row = "{},-".format(row)
                if "Data Sources:" in details:
                    row = "{},{}".format(row, str(re.findall(r"Data Sources: ([^\,]+)\,", details)[0]))
                else:
                    row = "{},-".format(row)
                if "Defense Bypassed:" in details:
                    row = "{},{}".format(row, str(re.findall(r"Defense Bypassed: ([^\,]+)\,", details)[0]))
                else:
                    row = "{},-".format(row)
                row = "{},{}".format(row, re.findall(r"Version: ([^\,]+)\,", details)[0])
                row = "{},{}".format(row, re.findall(r"Created: ([^\,]+)\,", details)[0])
                row = "{},{}".format(row, re.findall(r"Last Modified: (\d{1,2} [^\ ]+ \d{4})", details)[0])
                if "Detection:" in details:
                    if len(re.findall(r"Detection: ([^\,]*)", details)) > 0:
                        row = "{},{}".format(row, re.findall(r"Detection: ([^\,]*)", details)[0])
                    else:
                        row = "{},-".format(row)
                else:
                    row = "{},-".format(row)
                if "Mitigations:" in details:
                    if len(re.findall(r"Mitigations: ([^\,]*)", details)) > 0:
                        if len(re.findall(r"Mitigations: ([^\,]*)", details)[0]) > 1:
                            row = "{},{}".format(row, re.findall(r"Mitigations: ([^\,]*)", details)[0])
                        else:
                            row = "{},-".format(row)
                    else:
                        row = "{},-".format(row)
                else:
                    row = "{},-".format(row)
                if "Software:" in details:
                    if len(re.findall(r"Software: ([^\,]*)", details)) > 0:
                        if len(re.findall(r"Software: ([^\,]*)", details)[0]) > 1:
                            row = "{},{}".format(row, re.findall(r"Software: ([^\,]*)", details)[0])
                        else:
                            row = "{},-".format(row)
                    else:
                        row = "{},-".format(row)
                else:
                    row = "{},-".format(row)
                if len(eachvalue.strip()) > 0:
                    row = "{},{}\n".format(row, eachvalue.strip())
                else:
                    row = "{},-\n".format(row)
                mitrecsv.write(row.replace("\\\\","\\"))

if __name__ == '__main__':
	main()
