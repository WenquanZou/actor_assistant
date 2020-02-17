import spacy
import os
from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as ET

TEMPLATE_DIR = os.path.abspath('static')
app = Flask(__name__, template_folder=TEMPLATE_DIR)
nlp = None
MODEL = 'en_core_web_sm'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tokenise', methods=['POST'])
def tokenise():
    if not request.json or 'text' not in request.json:
        return jsonify({'success': False, 'error': 'Text not found.'}), 400

    text = request.json['text']
    ext = request.json['extension'] if 'extension' in request.json else ''
    meta = {}

    if ext == 'xml':
        text, meta = extract_xml(text)

    # Extract tokens from spaCy
    tokens = nlp.extract_tokens(text)
    return jsonify({'success': True, 'data': tokens, 'meta': meta})


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


def extract_xml(text):
    root = ET.fromstring(text)

    text = ""
    for child in root.find('./text'):
        if child.tag == 'p':
            text += child.text
            text += '\n\n'

    meta = {'title': concat_elements(root, './title'),
            'headline': concat_elements(root, './headline'),
            'date': root.attrib['date']}

    return text, meta


def concat_elements(root, tag):
    return ' '.join(map(lambda i: i.text, root.findall(tag)))


class NLP:
    def __init__(self):
        self.nlp = spacy.load(MODEL)
        print("spaCy loaded.")

    def extract_tokens(self, text):
        doc = self.nlp(text)
        return list(map(lambda token: token.text, doc))


if __name__ == '__main__':
    
    text = """<?xml version="1.0" encoding="UTF-8" ?>
<?xml-stylesheet type="text/xsl" href="file.xsl"?>

<play variant="ps" unique="alls-well-that-ends-well">
<title short="All&#8217;s Well That Ends Well">All&#8217;s Well That Ends Well</title>
<playwrights>
		<playwright>William Shakespeare</playwright>
		<playwright>Thomas Middleton</playwright>
</playwrights>
<pubdate>1605</pubdate>
<revdate>1622</revdate>



<statistics>
<category type="genre">Comedy</category>
</statistics>

<personae playtitle="All&#8217;s Well That Ends Well">

<persona gender="male" archetype="hero" id="f0a503de-1eb6-430e-84e9-0cc157f0f4c3">
<persname short="KING." numberOfLines="373" numberOfVerseLines="366" numberOfProseLines="7" numberOfLyricsLines="0">King of France</persname>
</persona>

<persona gender="male" id="e4b51df2-2a4c-45d4-a657-4130838ebcfc">
<persname short="BER." numberOfLines="240" numberOfVerseLines="199" numberOfProseLines="41" numberOfLyricsLines="0">Bertram, Count of Roussillon</persname>
</persona>

<persona gender="male" archetype="clown" id="0d19dfab-51a6-4e51-9a58-1d899d1dafb5">
<persname short="PAR." numberOfLines="184" numberOfVerseLines="58" numberOfProseLines="126" numberOfLyricsLines="0">Parolles</persname>
</persona>

<persona gender="male" id="df4e2ad0-6dcc-46f1-af74-c3c99d483ce2">
<persname short="LAF." numberOfLines="146" numberOfVerseLines="64" numberOfProseLines="82" numberOfLyricsLines="0">Lafew</persname>
</persona>

<persona gender="male" archetype="clown" id="9f513b4c-b30a-4efe-b082-2a133a0042ff">
<persname short="CLO." numberOfLines="74" numberOfVerseLines="15" numberOfProseLines="59" numberOfLyricsLines="14">Lavatch</persname>
</persona>

<persona gender="male" id="ede8c958-ccb1-4ccb-9385-39cc3fc6aa18">
<persname short="STEW." numberOfLines="23" numberOfVerseLines="19" numberOfProseLines="4" numberOfLyricsLines="0">Rinaldo</persname>
</persona>

<persona gender="male" id="a6a2517e-b033-4103-a8c5-b27994fc4474">
<persname short="DUKE." numberOfLines="19" numberOfVerseLines="19" numberOfProseLines="0" numberOfLyricsLines="0">Duke of Florence</persname>
</persona>

<persona gender="female" archetype="hero" id="033d23a3-2998-489c-b4a7-c254b994155d">
<persname short="HEL." numberOfLines="460" numberOfVerseLines="438" numberOfProseLines="22" numberOfLyricsLines="0">Helena</persname>
</persona>

<persona gender="female" archetype="hero" id="ee491ff4-9d43-4e07-9a75-fabfbf07878c">
<persname short="COUNT." numberOfLines="220" numberOfVerseLines="169" numberOfProseLines="51" numberOfLyricsLines="0">Countess of Roussillon</persname>
</persona>

<persona gender="female" id="5a136d39-d258-4078-a54d-ecb5a576667c">
<persname short="DIA." numberOfLines="137" numberOfVerseLines="134" numberOfProseLines="3" numberOfLyricsLines="0">Diana</persname>
</persona>

<persona gender="female" id="4a2fbd89-cc9e-41cd-b043-46c0c1c27087">
<persname short="WID." numberOfLines="56" numberOfVerseLines="51" numberOfProseLines="5" numberOfLyricsLines="0">An Old Widow of Florence</persname>
<persaliases>
	<persname short="BOTH MAR. AND WID.">Both Mariana and Widow</persname>
</persaliases>
</persona>

<persona gender="female" id="be61d1d5-da28-42c0-b9f8-1be9f80b6f9c">
<persname short="MAR." numberOfLines="6" numberOfVerseLines="2" numberOfProseLines="4" numberOfLyricsLines="0">Mariana</persname>
<persaliases>
	<persname short="BOTH MAR. AND WID.">Both Mariana and Widow</persname>
</persaliases>
</persona>

<persona gender="male" id="fb9d9e28-c77b-4111-bac1-fd4716138fee">
<persname short="1. LORD. DUM." numberOfLines="70" numberOfVerseLines="33" numberOfProseLines="37" numberOfLyricsLines="0">First French Lord Dumaine</persname>
<persaliases>
	<persname short="BOTH LORDS.">Both French Lords</persname>
</persaliases>
</persona>

<persona gender="male" id="9ce15e84-1106-4254-b4bd-fbfd3d3d690a">
<persname short="2. LORD. DUM." numberOfLines="80" numberOfVerseLines="34" numberOfProseLines="46" numberOfLyricsLines="0">Second French Lord Dumaine</persname>
<persaliases>
	<persname short="BOTH LORDS.">Both French Lords</persname>
</persaliases>
</persona>

<persona gender="male" id="6aa463e3-5682-4a1f-a710-c35f1fdb0974">
<persname short="1. SOLD. AS INTERPRETER." numberOfLines="53" numberOfVerseLines="18" numberOfProseLines="35" numberOfLyricsLines="0">First Soldier as Interpreter</persname>
</persona>

<persona gender="male" id="2d30834d-a2cc-4bc3-85ff-d439bb98cda6">
<persname short="2. SOLD." numberOfLines="2" numberOfVerseLines="2" numberOfProseLines="0" numberOfLyricsLines="0">Second Soldier</persname>
</persona>

<persona gender="male" id="844267de-ebb5-4638-aea9-75eb0c754bf0">
<persname short="GENT." numberOfLines="22" numberOfVerseLines="22" numberOfProseLines="0" numberOfLyricsLines="0">Gentleman</persname>
</persona>

<persona gender="male" id="9006a178-c3de-44d0-9c7a-87ed0077c2be">
<persname short="1. LORD." numberOfLines="2" numberOfVerseLines="2" numberOfProseLines="0" numberOfLyricsLines="0">First French Lord</persname>
<persaliases>
	<persname short="ALL LORDS.">All Lords</persname>
</persaliases>
</persona>

<persona gender="male" id="f1e15c83-43c1-47e0-a607-752b095ff86c">
<persname short="2. LORD." numberOfLines="2" numberOfVerseLines="2" numberOfProseLines="0" numberOfLyricsLines="0">Second French Lord</persname>
<persaliases>
	<persname short="ALL LORDS.">All French Lords</persname>
</persaliases>
</persona>

<persona gender="male" id="cab9fc17-65a1-40ea-a85b-b4c562b60ef4">
<persname short="3. LORD." numberOfLines="1" numberOfVerseLines="1" numberOfProseLines="0" numberOfLyricsLines="0">Third French Lord</persname>
<persaliases>
	<persname short="ALL LORDS.">All French Lords</persname>
</persaliases>
</persona>

<persona gender="male" id="490e7233-09f6-4e87-a673-496f98784320">
<persname short="4. LORD." numberOfLines="2" numberOfVerseLines="2" numberOfProseLines="0" numberOfLyricsLines="0">Fourth French Lord</persname>
<persaliases>
	<persname short="ALL LORDS.">All French Lords</persname>
</persaliases>
</persona>

<persona gender="male" id="6407aa16-302e-4a83-ac8c-a58937941a48">
<persname short="PAGE." numberOfLines="1" numberOfVerseLines="0" numberOfProseLines="1" numberOfLyricsLines="0">Countess&#8217;s Page</persname>
</persona>

<persona gender="male" id="f016e062-43a6-445f-a95e-581cef21ef2a">
<persname short="MESS." numberOfLines="1" numberOfVerseLines="0" numberOfProseLines="1" numberOfLyricsLines="0">Messenger</persname>
</persona>

<persona gender="female" id="72834791-8d5b-4a70-af0d-6d2594612ef1">
<persname short="VIOL." numberOfLines="0" numberOfVerseLines="0" numberOfProseLines="0" numberOfLyricsLines="0">Violenta</persname>
</persona>

</personae>

<act num="1">
<acttitle>Act 1</acttitle>
<scene actnum="1" num="1">
<scenetitle>Scene 1</scenetitle>
<scenelocation>Roussillon. A room in the Count&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="BER.">Bertram Count of Roussillon</scenepersona>
	<scenepersona short="COUNT.">Countess of Roussillon</scenepersona>
	<scenepersona short="HEL.">Helena</scenepersona>
	<scenepersona short="LAF.">Lord Lafew</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
	<scenepersona short="PAGE.">Page</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="fr">French</language>
</scenelanguage>


<stagedir sdglobalnumber="0.01" sdnumber="0.01">
	<dir>Enter young Bertram, Count of Roussillon, his mother the Countess of Roussillon, and Helena, Lord Lafew, all in black.</dir>
	<action type="enter">
		<actor>BER.</actor>
		<actor>COUNT.</actor>
		<actor>HEL.</actor>
		<actor>LAF.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1" number="1" form="prose">In delivering my son from me, I bury a second husband.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2" number="2" form="prose">And I in going, madam, weep o&#8217;er my father&#8217;s death anew; but I must attend his Majesty&#8217;s command, to whom I am now in ward, evermore in subjection.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="3" number="3" form="prose">You shall find of the King a husband, madam; you, sir, a father. He that so generally is at all times good must of necessity hold his virtue to you, whose worthiness would stir it up where it wanted rather than lack it where there is such abundance.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="4" number="4" form="prose">What hope is there of his Majesty&#8217;s amendment?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="5" number="5" form="prose">He hath abandon&#8217;d his physicians, madam, under whose practices he hath persecuted time with hope, and finds no other advantage in the process but only the losing of hope by time.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="6" number="6" form="prose">This young gentlewoman had a father&#8212;O, that &#8220;had,&#8221; how sad a passage &#8217;tis!&#8212;whose skill was almost as great as his honesty; had it stretch&#8217;d so far, would have made nature immortal, and death should have play for lack of work. Would for the King&#8217;s sake he were living! I think it would be the death of the King&#8217;s disease.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="7" number="7" form="prose">How call&#8217;d you the man you speak of, madam?</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="8" number="8" form="prose">He was famous, sir, in his profession, and it was his great right to be so&#8212;Gerard de Narbon.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="9" number="9" form="prose">He was excellent indeed, madam. The King very lately spoke of him admiringly and mourningly. He was skillful enough to have liv&#8217;d still, if knowledge could be set up against mortality.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="10" number="10" form="prose">What is it, my good lord, the King languishes of?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="11" number="11" form="prose">A fistula, my lord.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="12" number="12" form="prose">I heard not of it before.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="13" number="13" form="prose">I would it were not notorious. Was this gentlewoman the daughter of Gerard de Narbon?</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="14" number="14" form="prose">His sole child, my lord, and bequeath&#8217;d to my overlooking. I have those hopes of her good that her education promises her dispositions she inherits, which makes fair gifts fairer; for where an unclean mind carries virtuous qualities, there commendations go with pity: they are virtues and traitors too. In her they are the better for their simpleness; she derives her honesty, and achieves her goodness.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="15" number="15" form="prose">Your commendations, madam, get from her tears.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="16" number="16" form="prose">&#8217;Tis the best brine a maiden can season her praise in. The remembrance of her father never approaches her heart but the tyranny of her sorrows takes all livelihood from her cheek. No more of this, Helena; go to, no more, lest it be rather thought you affect a sorrow than to have&#8212;</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="17" number="17" form="prose">I do affect a sorrow indeed, but I have it too.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="18" number="18" form="prose">Moderate lamentation is the right of the dead, excessive grief the enemy to the living.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="19" number="19" form="prose">If the living be enemy to the grief, the excess makes it soon mortal.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="20" number="20" form="prose">Madam, I desire your holy wishes.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="21" number="21" form="prose">How understand we that?</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="22" number="22" form="verse">Be thou blest, Bertram, and succeed thy father</line>
<line globalnumber="23" number="23" form="verse">In manners as in shape! Thy blood and virtue</line>
<line globalnumber="24" number="24" form="verse">Contend for empire in thee, and thy goodness</line>
<line globalnumber="25" number="25" form="verse">Share with thy birthright! Love all, trust a few,</line>
<line globalnumber="26" number="26" form="verse">Do wrong to none. Be able for thine enemy</line>
<line globalnumber="27" number="27" form="verse">Rather in power than use, and keep thy friend</line>
<line globalnumber="28" number="28" form="verse">Under thy own life&#8217;s key. Be check&#8217;d for silence,</line>
<line globalnumber="29" number="29" form="verse">But never tax&#8217;d for speech. What heaven more will,</line>
<line globalnumber="30" number="30" form="verse">That thee may furnish, and my prayers pluck down,</line>
<line globalnumber="31" number="31" form="verse">Fall on thy head!&#8212;Farewell, my lord.</line>
<line globalnumber="32" number="32" form="verse">&#8217;Tis an unseason&#8217;d courtier, good my lord,</line>
<line globalnumber="33" number="33" form="verse" offset="0">Advise him.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="34" number="33" form="verse" offset="3">He cannot want the best</line>
<line globalnumber="35" number="34" form="verse" offset="0">That shall attend his love.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="36" number="34" form="verse" offset="5">Heaven bless him!</line>
<line globalnumber="37" number="35" form="verse" offset="0">Farewell, Bertram.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="38" number="35" form="verse" offset="4">The best wishes that can</line>
<line globalnumber="39" number="36" form="verse">Be forged in your thoughts be servants to you!</line>
<stagedir sdglobalnumber="39.01" sdnumber="36.01">
	<dir>Exit Countess.</dir>
	<action type="exit">
		<actor>COUNT.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="39.02" sdnumber="36.02">
	<dir>To Helena.</dir>
	<action type="speak">
		<actor>BER.</actor>
		<recipient>HEL.</recipient>
	</action>
</stagedir>
<line globalnumber="40" number="37" form="verse">Be comfortable to my mother, your mistress,</line>
<line globalnumber="41" number="38" form="verse" offset="0">And make much of her.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="42" number="38" form="verse" offset="5">Farewell, pretty lady,</line>
<line globalnumber="43" number="39" form="verse">You must hold the credit of your father.</line>
</speech>

<stagedir sdglobalnumber="43.01" sdnumber="39.01">
	<dir>Exeunt Bertram and Lafew.</dir>
	<action type="exit">
		<actor>BER.</actor>
		<actor>LAF.</actor>
	</action>
</stagedir>

<speech type="soliloquy">
<speaker long="Helena">HEL.</speaker>
<line globalnumber="44" number="40" form="verse">O, were that all! I think not on my father,</line>
<line globalnumber="45" number="41" form="verse">And these great tears grace his remembrance more</line>
<line globalnumber="46" number="42" form="verse">Than those I shed for him. What was he like?</line>
<line globalnumber="47" number="43" form="verse">I have forgot him. My imagination</line>
<line globalnumber="48" number="44" form="verse">Carries no favor in&#8217;t but Bertram&#8217;s.</line>
<line globalnumber="49" number="45" form="verse">I am undone, there is no living, none,</line>
<line globalnumber="50" number="46" form="verse">If Bertram be away. &#8217;Twere all one</line>
<line globalnumber="51" number="47" form="verse">That I should love a bright particular star</line>
<line globalnumber="52" number="48" form="verse">And think to wed it, he is so above me.</line>
<line globalnumber="53" number="49" form="verse">In this bright radiance and collateral light</line>
<line globalnumber="54" number="50" form="verse">Must I be comforted, not in his sphere.</line>
<line globalnumber="55" number="51" form="verse">Th&#8217; ambition in my love thus plagues itself:</line>
<line globalnumber="56" number="52" form="verse">The hind that would be mated by the lion</line>
<line globalnumber="57" number="53" form="verse">Must die for love. &#8217;Twas pretty, though a plague,</line>
<line globalnumber="58" number="54" form="verse">To see him every hour, to sit and draw</line>
<line globalnumber="59" number="55" form="verse">His arched brows, his hawking eye, his curls,</line>
<line globalnumber="60" number="56" form="verse">In our heart&#8217;s table&#8212;heart too capable</line>
<line globalnumber="61" number="57" form="verse">Of every line and trick of his sweet favor.</line>
<line globalnumber="62" number="58" form="verse">But now he&#8217;s gone, and my idolatrous fancy</line>
<line globalnumber="63" number="59" form="verse">Must sanctify his reliques. Who comes here?</line>
<stagedir sdglobalnumber="63.01" sdnumber="59.01">
	<dir>Enter Parolles.</dir>
	<action type="enter">
		<actor>PAR.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="63.02" sdnumber="59.02">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>HEL.</actor>
	</action>
</stagedir>
<line globalnumber="64" number="60" form="verse">One that goes with him. I love him for his sake,</line>
<line globalnumber="65" number="61" form="verse">And yet I know him a notorious liar,</line>
<line globalnumber="66" number="62" form="verse">Think him a great way fool, solely a coward;</line>
<line globalnumber="67" number="63" form="verse">Yet these fix&#8217;d evils sit so fit in him,</line>
<line globalnumber="68" number="64" form="verse">That they take place when virtue&#8217;s steely bones</line>
<line globalnumber="69" number="65" form="verse">Looks bleak i&#8217; th&#8217; cold wind. Withal, full oft we see</line>
<line globalnumber="70" number="66" form="verse">Cold wisdom waiting on superfluous folly.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="71" number="67" form="prose">&#8217;Save you, fair queen!</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="72" number="68" form="prose">And you, monarch!</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="73" number="69" form="prose">No.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="74" number="70" form="prose">And no.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="75" number="71" form="prose">Are you meditating on virginity?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="76" number="72" form="prose">Ay. You have some stain of soldier in you; let me ask a question. Man is enemy to virginity; how may we barricade it against him?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="77" number="73" form="prose">Keep him out.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="78" number="74" form="prose">But he assails, and our virginity though valiant, in the defense yet is weak. Unfold to us some warlike resistance.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="79" number="75" form="prose">There is none. Man, setting down before you, will undermine you and blow you up.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="80" number="76" form="prose">Bless our poor virginity from underminers and blowers-up! Is there no military policy how virgins might blow up men?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="81" number="77" form="prose">Virginity being blown down, man will quicklier be blown up. Marry, in blowing him down again, with the breach yourselves made, you lose your city. It is not politic in the commonwealth of nature to preserve virginity. Loss of virginity is rational increase, and there was never virgin got till virginity was first lost. That you were made of is metal to make virgins. Virginity, by being once lost, may be ten times found; by being ever kept, it is ever lost. &#8217;Tis too cold a companion; away with&#8217;t!</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="82" number="78" form="prose">I will stand for&#8217;t a little, though therefore I die a virgin.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="83" number="79" form="prose">There&#8217;s little can be said in&#8217;t, &#8217;tis against the rule of nature. To speak on the part of virginity is to accuse your mothers, which is most infallible disobedience. He that hangs himself is a virgin; virginity murders itself, and should be buried in highways out of all sanctified limit, as a desperate offendress against nature. Virginity breeds mites, much like a cheese, consumes itself to the very paring, and so dies with feeding his own stomach. Besides, virginity is peevish, proud, idle, made of self-love, which is the most inhibited sin in the canon. Keep it not, you cannot choose but lose by&#8217;t. Out with&#8217;t! Within t&#8217; one year it will make itself two, which is a goodly increase, and the principal itself not much the worse. Away with&#8217;t!</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="84" number="80" form="prose">How might one do, sir, to lose it to her own liking?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="85" number="81" form="prose">Let me see. Marry, ill, to like him that ne&#8217;er it likes. &#8217;Tis a commodity will lose the gloss with lying: the longer kept, the less worth. Off with&#8217;t while &#8217;tis vendible; answer the time of request. Virginity, like an old courtier, wears her cap out of fashion, richly suited, but unsuitable&#8212;just like the brooch and the toothpick, which wear not now. Your date is better in your pie and your porridge than in your cheek; and your virginity, your old virginity, is like one of our French wither&#8217;d pears, it looks ill, it eats drily, marry, &#8217;tis a wither&#8217;d pear; it was formerly better, marry, yet &#8217;tis a wither&#8217;d pear. Will you any thing with it?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="86" number="82" form="verse">Not my virginity yet:</line>
<line globalnumber="87" number="83" form="verse">There shall your master have a thousand loves,</line>
<line globalnumber="88" number="84" form="verse">A mother, and a mistress, and a friend,</line>
<line globalnumber="89" number="85" form="verse">A phoenix, captain, and an enemy,</line>
<line globalnumber="90" number="86" form="verse">A guide, a goddess, and a sovereign,</line>
<line globalnumber="91" number="87" form="verse">A counsellor, a traitress, and a dear;</line>
<line globalnumber="92" number="88" form="verse">His humble ambition, proud humility;</line>
<line globalnumber="93" number="89" form="verse">His jarring concord, and his discord dulcet;</line>
<line globalnumber="94" number="90" form="verse">His faith, his sweet disaster; with a world</line>
<line globalnumber="95" number="91" form="verse">Of pretty, fond, adoptions christendoms</line>
<line globalnumber="96" number="92" form="verse">That blinking Cupid gossips. Now shall he&#8212;</line>
<line globalnumber="97" number="93" form="verse">I know not what he shall&#8212;God send him well!</line>
<line globalnumber="98" number="94" form="verse">The court&#8217;s a learning place, and he is one&#8212;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="99" number="95" form="prose">What one, i&#8217; faith?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="100" number="96" form="prose">That I wish well. &#8217;Tis pity&#8212;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="101" number="97" form="prose">What&#8217;s pity?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="102" number="98" form="verse">That wishing well had not a body in&#8217;t,</line>
<line globalnumber="103" number="99" form="verse">Which might be felt, that we, the poorer born,</line>
<line globalnumber="104" number="100" form="verse">Whose baser stars do shut us up in wishes,</line>
<line globalnumber="105" number="101" form="verse">Might with effects of them follow our friends,</line>
<line globalnumber="106" number="102" form="verse">And show what we alone must think, which never</line>
<line globalnumber="107" number="103" form="verse">Returns us thanks.</line>
</speech>

<stagedir sdglobalnumber="107.01" sdnumber="103.01">
	<dir>Enter Page.</dir>
	<action type="enter">
		<actor>PAGE.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Countess&#8217;s Page">PAGE.</speaker>
<line globalnumber="108" number="104" form="prose"><foreign xml:lang="fr">Monsieur</foreign> Parolles, my lord calls for you.</line>
</speech>

<stagedir sdglobalnumber="108.01" sdnumber="104.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>PAGE.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="109" number="105" form="prose">Little Helen, farewell. If I can remember thee, I will think of thee at court.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="110" number="106" form="prose"><foreign xml:lang="fr">Monsieur</foreign> Parolles, you were born under a charitable star.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="111" number="107" form="prose">Under Mars, I.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="112" number="108" form="prose">I especially think, under Mars.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="113" number="109" form="prose">Why under Mars?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="114" number="110" form="prose">The wars hath so kept you under that you must needs be born under Mars.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="115" number="111" form="prose">When he was predominant.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="116" number="112" form="prose">When he was retrograde, I think rather.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="117" number="113" form="prose">Why think you so?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="118" number="114" form="prose">You go so much backward when you fight.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="119" number="115" form="prose">That&#8217;s for advantage.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="120" number="116" form="prose">So is running away, when fear proposes the safety. But the composition that your valor and fear makes in you is a virtue of a good wing, and I like the wear well.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="121" number="117" form="prose">I am so full of businesses, I cannot answer thee acutely. I will return perfect courtier, in the which my instruction shall serve to naturalize thee, so thou wilt be capable of a courtier&#8217;s counsel, and understand what advice shall thrust upon thee, else thou diest in thine unthankfulness, and thine ignorance makes thee away. Farewell. When thou hast leisure, say thy prayers; when thou hast none, remember thy friends. Get thee a good husband, and use him as he uses thee. So farewell.</line>
</speech>

<stagedir sdglobalnumber="121.01" sdnumber="117.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech type="soliloquy">
<speaker long="Helena">HEL.</speaker>
<line globalnumber="122" number="118" form="verse">Our remedies oft in ourselves do lie,</line>
<line globalnumber="123" number="119" form="verse">Which we ascribe to heaven. The fated sky</line>
<line globalnumber="124" number="120" form="verse">Gives us free scope, only doth backward pull</line>
<line globalnumber="125" number="121" form="verse">Our slow designs when we ourselves are dull.</line>
<line globalnumber="126" number="122" form="verse">What power is it which mounts my love so high,</line>
<line globalnumber="127" number="123" form="verse">That makes me see, and cannot feed mine eye?</line>
<line globalnumber="128" number="124" form="verse">The mightiest space in fortune nature brings</line>
<line globalnumber="129" number="125" form="verse">To join like likes, and kiss like native things.</line>
<line globalnumber="130" number="126" form="verse">Impossible be strange attempts to those</line>
<line globalnumber="131" number="127" form="verse">That weigh their pains in sense, and do suppose</line>
<line globalnumber="132" number="128" form="verse">What hath been cannot be. Who ever strove</line>
<line globalnumber="133" number="129" form="verse">To show her merit, that did miss her love?</line>
<line globalnumber="134" number="130" form="verse">The King&#8217;s disease&#8212;my project may deceive me,</line>
<line globalnumber="135" number="131" form="verse">But my intents are fix&#8217;d, and will not leave me.</line>
</speech>

<stagedir sdglobalnumber="135.01" sdnumber="131.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>HEL.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="1" num="2">
<scenetitle>Scene 2</scenetitle>
<scenelocation>Paris. The King&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="KING.">King of France</scenepersona>
	<scenepersona short="BOTH LORDS.">Lords</scenepersona>
	<scenepersona>Attendants</scenepersona>
	<scenepersona short="BER.">Bertram</scenepersona>
	<scenepersona short="LAF.">Lafew</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="135.02" sdnumber="0.01">
	<dir>Flourish cornets. Enter the King of France with letters, Lords, and diverse Attendants.</dir>
	<action type="sound">
	</action>
	<action type="enter">
		<actor>KING.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
		<actor>Attendants</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="136" number="1" form="verse">The Florentines and Senoys are by th&#8217; ears,</line>
<line globalnumber="137" number="2" form="verse">Have fought with equal fortune, and continue</line>
<line globalnumber="138" number="3" form="verse" offset="0">A braving war.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="139" number="3" form="verse" offset="3">So &#8217;tis reported, sir.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="140" number="4" form="verse">Nay, &#8217;tis most credible; we here receive it</line>
<line globalnumber="141" number="5" form="verse">A certainty, vouch&#8217;d from our cousin Austria,</line>
<line globalnumber="142" number="6" form="verse">With caution, that the Florentine will move us</line>
<line globalnumber="143" number="7" form="verse">For speedy aid; wherein our dearest friend</line>
<line globalnumber="144" number="8" form="verse">Prejudicates the business, and would seem</line>
<line globalnumber="145" number="9" form="verse" offset="0">To have us make denial.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="146" number="9" form="verse" offset="5">His love and wisdom,</line>
<line globalnumber="147" number="10" form="verse">Approv&#8217;d so to your Majesty, may plead</line>
<line globalnumber="148" number="11" form="verse" offset="0">For amplest credence.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="149" number="11" form="verse" offset="4">He hath arm&#8217;d our answer,</line>
<line globalnumber="150" number="12" form="verse">And Florence is denied before he comes.</line>
<line globalnumber="151" number="13" form="verse">Yet for our gentlemen that mean to see</line>
<line globalnumber="152" number="14" form="verse">The Tuscan service, freely have they leave</line>
<line globalnumber="153" number="15" form="verse" offset="0">To stand on either part.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="154" number="15" form="verse" offset="5">It well may serve</line>
<line globalnumber="155" number="16" form="verse">A nursery to our gentry, who are sick</line>
<line globalnumber="156" number="17" form="verse" offset="0">For breathing and exploit.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="157" number="17" form="verse" offset="5">What&#8217;s he comes here?</line>
</speech>

<stagedir sdglobalnumber="157.01" sdnumber="17.01">
	<dir>Enter Bertram, Lafew, and Parolles.</dir>
	<action type="enter">
		<actor>BER.</actor>
		<actor>LAF.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="158" number="18" form="verse">It is the Count Roussillon, my good lord,</line>
<line globalnumber="159" number="19" form="verse" offset="0">Young Bertram.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="160" number="19" form="verse" offset="3">Youth, thou bear&#8217;st thy father&#8217;s face;</line>
<line globalnumber="161" number="20" form="verse">Frank Nature, rather curious than in haste,</line>
<line globalnumber="162" number="21" form="verse">Hath well compos&#8217;d thee. Thy father&#8217;s moral parts</line>
<line globalnumber="163" number="22" form="verse">Mayst thou inherit too! Welcome to Paris.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="164" number="23" form="verse">My thanks and duty are your Majesty&#8217;s.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="165" number="24" form="verse">I would I had that corporal soundness now</line>
<line globalnumber="166" number="25" form="verse">As when thy father and myself in friendship</line>
<line globalnumber="167" number="26" form="verse">First tried our soldiership! He did look far</line>
<line globalnumber="168" number="27" form="verse">Into the service of the time, and was</line>
<line globalnumber="169" number="28" form="verse">Discipled of the bravest. He lasted long,</line>
<line globalnumber="170" number="29" form="verse">But on us both did haggish age steal on,</line>
<line globalnumber="171" number="30" form="verse">And wore us out of act. It much repairs me</line>
<line globalnumber="172" number="31" form="verse">To talk of your good father. In his youth</line>
<line globalnumber="173" number="32" form="verse">He had the wit which I can well observe</line>
<line globalnumber="174" number="33" form="verse">Today in our young lords; but they may jest</line>
<line globalnumber="175" number="34" form="verse">Till their own scorn return to them unnoted</line>
<line globalnumber="176" number="35" form="verse">Ere they can hide their levity in honor.</line>
<line globalnumber="177" number="36" form="verse">So like a courtier, contempt nor bitterness</line>
<line globalnumber="178" number="37" form="verse">Were in his pride or sharpness; if they were,</line>
<line globalnumber="179" number="38" form="verse">His equal had awak&#8217;d them, and his honor,</line>
<line globalnumber="180" number="39" form="verse">Clock to itself, knew the true minute when</line>
<line globalnumber="181" number="40" form="verse">Exception bid him speak, and at this time</line>
<line globalnumber="182" number="41" form="verse">His tongue obey&#8217;d his hand. Who were below him</line>
<line globalnumber="183" number="42" form="verse">He us&#8217;d as creatures of another place,</line>
<line globalnumber="184" number="43" form="verse">And bow&#8217;d his eminent top to their low ranks,</line>
<line globalnumber="185" number="44" form="verse">Making them proud of his humility,</line>
<line globalnumber="186" number="45" form="verse">In their poor praise he humbled. Such a man</line>
<line globalnumber="187" number="46" form="verse">Might be a copy to these younger times;</line>
<line globalnumber="188" number="47" form="verse">Which followed well, would demonstrate them now</line>
<line globalnumber="189" number="48" form="verse" offset="0">But goers backward.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="190" number="48" form="verse" offset="4">His good remembrance, sir,</line>
<line globalnumber="191" number="49" form="verse">Lies richer in your thoughts than on his tomb.</line>
<line globalnumber="192" number="50" form="verse">So in approof lives not his epitaph</line>
<line globalnumber="193" number="51" form="verse">As in your royal speech.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="194" number="52" form="verse">Would I were with him! He would always say&#8212;</line>
<line globalnumber="195" number="53" form="verse">Methinks I hear him now; his plausive words</line>
<line globalnumber="196" number="54" form="verse">He scatter&#8217;d not in ears, but grafted them,</line>
<line globalnumber="197" number="55" form="verse">To grow there and to bear&#8212;&#8220;Let me not live&#8221;&#8212;</line>
<line globalnumber="198" number="56" form="verse">This his good melancholy oft began,</line>
<line globalnumber="199" number="57" form="verse">On the catastrophe and heel of pastime,</line>
<line globalnumber="200" number="58" form="verse">When it was out&#8212;&#8220;Let me not live,&#8221; quoth he,</line>
<line globalnumber="201" number="59" form="verse">&#8220;After my flame lacks oil, to be the snuff</line>
<line globalnumber="202" number="60" form="verse">Of younger spirits, whose apprehensive senses</line>
<line globalnumber="203" number="61" form="verse">All but new things disdain; whose judgments are</line>
<line globalnumber="204" number="62" form="verse">Mere fathers of their garments; whose constancies</line>
<line globalnumber="205" number="63" form="verse">Expire before their fashions.&#8221; This he wish&#8217;d.</line>
<line globalnumber="206" number="64" form="verse">I, after him, do after him wish too,</line>
<line globalnumber="207" number="65" form="verse">Since I nor wax nor honey can bring home,</line>
<line globalnumber="208" number="66" form="verse">I quickly were dissolved from my hive,</line>
<line globalnumber="209" number="67" form="verse" offset="0">To give some laborers room.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="210" number="67" form="verse" offset="5">You&#8217;re loved, sir;</line>
<line globalnumber="211" number="68" form="verse">They that least lend it you shall lack you first.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="212" number="69" form="verse">I fill a place, I know&#8217;t. How long is&#8217;t, Count,</line>
<line globalnumber="213" number="70" form="verse">Since the physician at your father&#8217;s died?</line>
<line globalnumber="214" number="71" form="verse" offset="0">He was much fam&#8217;d.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="215" number="71" form="verse" offset="4">Some six months since, my lord.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="216" number="72" form="verse">If he were living, I would try him yet.&#8212;</line>
<line globalnumber="217" number="73" form="verse">Lend me an arm.&#8212;The rest have worn me out</line>
<line globalnumber="218" number="74" form="verse">With several applications. Nature and sickness</line>
<line globalnumber="219" number="75" form="verse">Debate it at their leisure. Welcome, Count,</line>
<line globalnumber="220" number="76" form="verse" offset="0">My son&#8217;s no dearer.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="221" number="76" form="verse" offset="4">Thank your Majesty.</line>
</speech>

<stagedir sdglobalnumber="221.01" sdnumber="76.01">
	<dir>Exeunt. Flourish.</dir>
	<action type="exit">
		<actor>BER.</actor>
		<actor>LAF.</actor>
		<actor>PAR.</actor>
		<actor>KING.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
		<actor>Attendants</actor>
	</action>
</stagedir>

</scene>

<scene actnum="1" num="3">
<scenetitle>Scene 3</scenetitle>
<scenelocation>Roussillon. A room in the Count&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="COUNT.">Countess</scenepersona>
	<scenepersona short="STEW.">Steward Rinaldo</scenepersona>
	<scenepersona short="CLO.">Clown Lavatch</scenepersona>
	<scenepersona short="HEL.">Helen</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="la">Latin</language>
</scenelanguage>


<stagedir sdglobalnumber="221.02" sdnumber="0.01">
	<dir>Enter Countess, Steward Rinaldo, and Clown Lavatch.</dir>
	<action type="enter">
		<actor>COUNT.</actor>
		<actor>STEW.</actor>
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="222" number="1" form="prose">I will now hear. What say you of this gentlewoman?</line>
</speech>

<speech>
<speaker long="Rinaldo">STEW.</speaker>
<line globalnumber="223" number="2" form="prose">Madam, the care I have had to even your content, I wish might be found in the calendar of my past endeavors, for then we wound our modesty, and make foul the clearness of our deservings, when of ourselves we publish them.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="224" number="3" form="prose">What does this knave here? Get you gone, sirrah. The complaints I have heard of you I do not all believe. &#8217;Tis my slowness that I do not, for I know you lack not folly to commit them, and have ability enough to make such knaveries yours.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="225" number="4" form="prose">&#8217;Tis not unknown to you, madam, I am a poor fellow.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="226" number="5" form="prose">Well, sir.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="227" number="6" form="prose">No, madam, &#8217;tis not so well that I am poor, though many of the rich are damn&#8217;d, but if I may have your ladyship&#8217;s good will to go to the world, Isbel the woman and I will do as we may.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="228" number="7" form="prose">Wilt thou needs be a beggar?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="229" number="8" form="prose">I do beg your good will in this case.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="230" number="9" form="prose">In what case?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="231" number="10" form="prose">In Isbel&#8217;s case and mine own. Service is no heritage, and I think I shall never have the blessing of God till I have issue a&#8217; my body; for they say barnes are blessings.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="232" number="11" form="prose">Tell me thy reason why thou wilt marry.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="233" number="12" form="prose">My poor body, madam, requires it. I am driven on by the flesh, and he must needs go that the devil drives.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="234" number="13" form="prose">Is this all your worship&#8217;s reason?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="235" number="14" form="prose">Faith, madam, I have other holy reasons, such as they are.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="236" number="15" form="prose">May the world know them?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="237" number="16" form="prose">I have been, madam, a wicked creature, as you and all flesh and blood are, and indeed I do marry that I may repent.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="238" number="17" form="prose">Thy marriage, sooner than thy wickedness.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="239" number="18" form="prose">I am out a&#8217; friends, madam, and I hope to have friends for my wive&#8217;s sake.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="240" number="19" form="prose">Such friends are thine enemies, knave.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="241" number="20" form="prose">Y&#8217; are shallow, madam&#8212;in great friends, for the knaves come to do that for me which I am a-weary of. He that ears my land spares my team, and gives me leave to inn the crop. If I be his cuckold, he&#8217;s my drudge. He that comforts my wife is the cherisher of my flesh and blood; he that cherishes my flesh and blood loves my flesh and blood; he that loves my flesh and blood is my friend: <foreign xml:lang="la">ergo</foreign>, he that kisses my wife is my friend. If men could be contented to be what they are, there were no fear in marriage, for young Charbon the puritan and old Poysam the papist, howsome&#8217;er their hearts are sever&#8217;d in religion, their heads are both one: they may jowl horns together like any deer i&#8217; th&#8217; herd.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="242" number="21" form="prose">Wilt thou ever be a foul-mouth&#8217;d and calumnious knave?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="243" number="22" form="prose">A prophet I, madam, and I speak the truth the next way:</line>
<line globalnumber="244" number="23" form="verse" type="lyric">For I the ballad will repeat,</line>
<line globalnumber="245" number="24" form="verse" type="lyric">Which men full true shall find:</line>
<line globalnumber="246" number="25" form="verse" type="lyric">Your marriage comes by destiny,</line>
<line globalnumber="247" number="26" form="verse" type="lyric">Your cuckoo sings by kind.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="248" number="27" form="prose">Get you gone, sir, I&#8217;ll talk with you more anon.</line>
</speech>

<speech>
<speaker long="Rinaldo">STEW.</speaker>
<line globalnumber="249" number="28" form="prose">May it please you, madam, that he bid Helen come to you. Of her I am to speak.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="250" number="29" form="prose">Sirrah, tell my gentlewoman I would speak with her&#8212;Helen, I mean.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>

<stagedir sdglobalnumber="250.01" sdnumber="29.01">
	<dir>Sings.</dir>
	<action type="song">
		<actor>CLO.</actor>
	</action>
</stagedir>
<line globalnumber="251" number="30" form="verse" type="lyric">&#8220;Was this fair face the cause,&#8221; quoth she,</line>
<line globalnumber="252" number="31" form="verse" type="lyric">&#8220;Why the Grecians sacked Troy?</line>
<line globalnumber="253" number="32" form="verse" type="lyric">Fond done, done fond,</line>
<line globalnumber="254" number="33" form="verse" type="lyric">Was this King Priam&#8217;s joy?&#8221;</line>
<line globalnumber="255" number="34" form="verse" type="lyric">With that she sighed as she stood,</line>
<line globalnumber="256" number="35" form="verse" type="lyric">With that she sighed as she stood,</line>
<line globalnumber="257" number="36" form="verse" type="lyric">And gave this sentence then:</line>
<line globalnumber="258" number="37" form="verse" type="lyric">&#8220;Among nine bad if one be good,</line>
<line globalnumber="259" number="38" form="verse" type="lyric">Among nine bad if one be good,</line>
<line globalnumber="260" number="39" form="verse" type="lyric">There&#8217;s yet one good in ten.&#8221;</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="261" number="40" form="prose">What, one good in ten? You corrupt the song, sirrah.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="262" number="41" form="prose">One good woman in ten, madam, which is a purifying a&#8217; th&#8217; song. Would God would serve the world so all the year! We&#8217;d find no fault with the tithe-woman if I were the parson. One in ten, quoth &#8217;a? And we might have a good woman born but or every blazing star or at an earthquake, &#8217;twould mend the lottery well; a man may draw his heart out ere &#8217;a pluck one.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="263" number="42" form="prose">You&#8217;ll be gone, sir knave, and do as I command you.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="264" number="43" form="prose">That man should be at woman&#8217;s command, and yet no hurt done! Though honesty be no puritan, yet it will do no hurt; it will wear the surplice of humility over the black gown of a big heart. I am going, forsooth. The business is for Helen to come hither.</line>
</speech>

<stagedir sdglobalnumber="264.01" sdnumber="43.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="265" number="44" form="prose">Well, now.</line>
</speech>

<speech>
<speaker long="Rinaldo">STEW.</speaker>
<line globalnumber="266" number="45" form="prose">I know, madam, you love your gentlewoman entirely.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="267" number="46" form="prose">Faith, I do. Her father bequeath&#8217;d her to me, and she herself, without other advantage, may lawfully make title to as much love as she finds. There is more owing her than is paid, and more shall be paid her than she&#8217;ll demand.</line>
</speech>

<speech>
<speaker long="Rinaldo">STEW.</speaker>
<line globalnumber="268" number="47" form="prose">Madam, I was very late more near her than I think she wish&#8217;d me. Alone she was, and did communicate to herself her own words to her own ears; she thought, I dare vow for her, they touch&#8217;d not any stranger sense. Her matter was, she lov&#8217;d your son. Fortune, she said, was no goddess, that had put such difference betwixt their two estates; Love no god, that would not extend his might only where qualities were level; Diana no queen of virgins, that would suffer her poor knight surpris&#8217;d without rescue in the first assault or ransom afterward. This she deliver&#8217;d in the most bitter touch of sorrow that e&#8217;er I heard virgin exclaim in, which I held my duty speedily to acquaint you withal, sithence in the loss that may happen, it concerns you something to know it.</line>
</speech>

<speech type="soliloquy">
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="269" number="48" form="prose">You have discharg&#8217;d this honestly, keep it to yourself. Many likelihoods inform&#8217;d me of this before, which hung so tott&#8217;ring in the balance that I could neither believe nor misdoubt. Pray you leave me. Stall this in your bosom, and I thank you for your honest care. I will speak with you further anon.</line>
<stagedir sdglobalnumber="269.01" sdnumber="48.01">
	<dir>Exit Steward.</dir>
	<action type="exit">
		<actor>STEW.</actor>
	</action>
</stagedir>
<stagedir sdglobalnumber="269.02" sdnumber="48.02">
	<dir>Enter Helen.</dir>
	<action type="enter">
		<actor>HEL.</actor>
	</action>
</stagedir>
<line globalnumber="270" number="49" form="verse">Even so it was with me when I was young.</line>
<line globalnumber="271" number="50" form="verse">If ever we are nature&#8217;s, these are ours. This thorn</line>
<line globalnumber="272" number="51" form="verse">Doth to our rose of youth rightly belong;</line>
<line globalnumber="273" number="52" form="verse">Our blood to us, this to our blood is born.</line>
<line globalnumber="274" number="53" form="verse">It is the show and seal of nature&#8217;s truth,</line>
<line globalnumber="275" number="54" form="verse">Where love&#8217;s strong passion is impress&#8217;d in youth.</line>
<line globalnumber="276" number="55" form="verse">By our remembrances of days foregone,</line>
<line globalnumber="277" number="56" form="verse">Such were our faults, or then we thought them none.</line>
<line globalnumber="278" number="57" form="verse">Her eye is sick on&#8217;t; I observe her now.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="279" number="58" form="verse" offset="0">What is your pleasure, madam?</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="280" number="58" form="verse" offset="6">You know, Helen,</line>
<line globalnumber="281" number="59" form="verse">I am a mother to you.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="282" number="60" form="verse" offset="0">Mine honorable mistress.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="283" number="60" form="verse" offset="5">Nay, a mother,</line>
<line globalnumber="284" number="61" form="verse">Why not a mother? When I said &#8220;a mother,&#8221;</line>
<line globalnumber="285" number="62" form="verse">Methought you saw a serpent. What&#8217;s in &#8220;mother,&#8221;</line>
<line globalnumber="286" number="63" form="verse">That you start at it? I say I am your mother,</line>
<line globalnumber="287" number="64" form="verse">And put you in the catalogue of those</line>
<line globalnumber="288" number="65" form="verse">That were enwombed mine. &#8217;Tis often seen</line>
<line globalnumber="289" number="66" form="verse">Adoption strives with nature, and choice breeds</line>
<line globalnumber="290" number="67" form="verse">A native slip to us from foreign seeds.</line>
<line globalnumber="291" number="68" form="verse">You ne&#8217;er oppress&#8217;d me with a mother&#8217;s groan,</line>
<line globalnumber="292" number="69" form="verse">Yet I express to you a mother&#8217;s care.</line>
<line globalnumber="293" number="70" form="verse">God&#8217;s mercy, maiden! Does it curd thy blood</line>
<line globalnumber="294" number="71" form="verse">To say I am thy mother? What&#8217;s the matter,</line>
<line globalnumber="295" number="72" form="verse">That this distempered messenger of wet,</line>
<line globalnumber="296" number="73" form="verse">The many-color&#8217;d Iris, rounds thine eye?</line>
<line globalnumber="297" number="74" form="verse" offset="0">&#8212;Why, that you are my daughter?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="298" number="74" form="verse" offset="7">That I am not.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="299" number="75" form="verse" offset="0">I say I am your mother.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="300" number="75" form="verse" offset="5">Pardon, madam;</line>
<line globalnumber="301" number="76" form="verse">The Count Roussillon cannot be my brother:</line>
<line globalnumber="302" number="77" form="verse">I am from humble, he from honored name;</line>
<line globalnumber="303" number="78" form="verse">No note upon my parents, his all noble.</line>
<line globalnumber="304" number="79" form="verse">My master, my dear lord he is, and I</line>
<line globalnumber="305" number="80" form="verse">His servant live, and will his vassal die.</line>
<line globalnumber="306" number="81" form="verse" offset="0">He must not be my brother.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="307" number="81" form="verse" offset="5">Nor I your mother?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="308" number="82" form="verse">You are my mother, madam; would you were&#8212;</line>
<line globalnumber="309" number="83" form="verse">So that my lord your son were not my brother&#8212;</line>
<line globalnumber="310" number="84" form="verse">Indeed my mother! Or were you both our mothers,</line>
<line globalnumber="311" number="85" form="verse">I care no more for than I do for heaven,</line>
<line globalnumber="312" number="86" form="verse">So I were not his sister. Can&#8217;t no other,</line>
<line globalnumber="313" number="87" form="verse">But, I your daughter, he must be my brother?</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="314" number="88" form="verse">Yes, Helen, you might be my daughter-in-law.</line>
<line globalnumber="315" number="89" form="verse">God shield you mean it not! &#8220;daughter&#8221; and &#8220;mother&#8221;</line>
<line globalnumber="316" number="90" form="verse">So strive upon your pulse. What, pale again?</line>
<line globalnumber="317" number="91" form="verse">My fear hath catch&#8217;d your fondness! Now I see</line>
<line globalnumber="318" number="92" form="verse">The myst&#8217;ry of your loneliness, and find</line>
<line globalnumber="319" number="93" form="verse">Your salt tears&#8217; head, now to all sense &#8217;tis gross:</line>
<line globalnumber="320" number="94" form="verse">You love my son. Invention is asham&#8217;d,</line>
<line globalnumber="321" number="95" form="verse">Against the proclamation of thy passion,</line>
<line globalnumber="322" number="96" form="verse">To say thou dost not: therefore tell me true,</line>
<line globalnumber="323" number="97" form="verse">But tell me then &#8217;tis so; for look, thy cheeks</line>
<line globalnumber="324" number="98" form="verse">Confess it, t&#8217; one to th&#8217; other, and thine eyes</line>
<line globalnumber="325" number="99" form="verse">See it so grossly shown in thy behaviors</line>
<line globalnumber="326" number="100" form="verse">That in their kind they speak it. Only sin</line>
<line globalnumber="327" number="101" form="verse">And hellish obstinacy tie thy tongue,</line>
<line globalnumber="328" number="102" form="verse">That truth should be suspected. Speak, is&#8217;t so?</line>
<line globalnumber="329" number="103" form="verse">If it be so, you have wound a goodly clew;</line>
<line globalnumber="330" number="104" form="verse">If it be not, forswear&#8217;t; howe&#8217;er, I charge thee,</line>
<line globalnumber="331" number="105" form="verse">As heaven shall work in me for thine avail,</line>
<line globalnumber="332" number="106" form="verse" offset="0">To tell me truly.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="333" number="106" form="verse" offset="5">Good madam, pardon me!</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="334" number="107" form="verse" offset="0">Do you love my son?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="335" number="107" form="verse" offset="5">Your pardon, noble mistress!</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="336" number="108" form="verse" offset="0">Love you my son?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="337" number="108" form="verse" offset="4">Do not you love him, madam?</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="338" number="109" form="verse">Go not about; my love hath in&#8217;t a bond</line>
<line globalnumber="339" number="110" form="verse">Whereof the world takes note. Come, come, disclose</line>
<line globalnumber="340" number="111" form="verse">The state of your affection, for your passions</line>
<line globalnumber="341" number="112" form="verse" offset="0">Have to the full appeach&#8217;d.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="342" number="112" form="verse" offset="6">Then I confess</line>
<line globalnumber="343" number="113" form="verse">Here on my knee, before high heaven and you,</line>
<line globalnumber="344" number="114" form="verse">That before you, and next unto high heaven,</line>
<line globalnumber="345" number="115" form="verse">I love your son.</line>
<line globalnumber="346" number="116" form="verse">My friends were poor, but honest, so&#8217;s my love.</line>
<line globalnumber="347" number="117" form="verse">Be not offended, for it hurts not him</line>
<line globalnumber="348" number="118" form="verse">That he is lov&#8217;d of me; I follow him not</line>
<line globalnumber="349" number="119" form="verse">By any token of presumptuous suit,</line>
<line globalnumber="350" number="120" form="verse">Nor would I have him till I do deserve him,</line>
<line globalnumber="351" number="121" form="verse">Yet never know how that desert should be.</line>
<line globalnumber="352" number="122" form="verse">I know I love in vain, strive against hope;</line>
<line globalnumber="353" number="123" form="verse">Yet in this captious and intenible sieve</line>
<line globalnumber="354" number="124" form="verse">I still pour in the waters of my love</line>
<line globalnumber="355" number="125" form="verse">And lack not to lose still. Thus Indian-like,</line>
<line globalnumber="356" number="126" form="verse">Religious in mine error, I adore</line>
<line globalnumber="357" number="127" form="verse">The sun, that looks upon his worshipper,</line>
<line globalnumber="358" number="128" form="verse">But knows of him no more. My dearest madam,</line>
<line globalnumber="359" number="129" form="verse">Let not your hate encounter with my love</line>
<line globalnumber="360" number="130" form="verse">For loving where you do; but if yourself,</line>
<line globalnumber="361" number="131" form="verse">Whose aged honor cites a virtuous youth,</line>
<line globalnumber="362" number="132" form="verse">Did ever in so true a flame of liking</line>
<line globalnumber="363" number="133" form="verse">Wish chastely, and love dearly, that your Dian</line>
<line globalnumber="364" number="134" form="verse">Was both herself and Love, O then give pity</line>
<line globalnumber="365" number="135" form="verse">To her whose state is such that cannot choose</line>
<line globalnumber="366" number="136" form="verse">But lend and give where she is sure to lose;</line>
<line globalnumber="367" number="137" form="verse">That seeks not to find that her search implies,</line>
<line globalnumber="368" number="138" form="verse">But riddle-like lives sweetly where she dies.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="369" number="139" form="verse">Had you not lately an intent&#8212;speak truly&#8212;</line>
<line globalnumber="370" number="140" form="verse" offset="0">To go to Paris?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="371" number="140" form="verse" offset="4">Madam, I had.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="372" number="140" form="verse" offset="7">Wherefore? Tell true.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="373" number="141" form="verse">I will tell truth, by grace itself I swear.</line>
<line globalnumber="374" number="142" form="verse">You know my father left me some prescriptions</line>
<line globalnumber="375" number="143" form="verse">Of rare and prov&#8217;d effects, such as his reading</line>
<line globalnumber="376" number="144" form="verse">And manifest experience had collected</line>
<line globalnumber="377" number="145" form="verse">For general sovereignty; and that he will&#8217;d me</line>
<line globalnumber="378" number="146" form="verse">In heedfull&#8217;st reservation to bestow them,</line>
<line globalnumber="379" number="147" form="verse">As notes whose faculties inclusive were</line>
<line globalnumber="380" number="148" form="verse">More than they were in note. Amongst the rest,</line>
<line globalnumber="381" number="149" form="verse">There is a remedy, approv&#8217;d, set down,</line>
<line globalnumber="382" number="150" form="verse">To cure the desperate languishings whereof</line>
<line globalnumber="383" number="151" form="verse" offset="0">The King is render&#8217;d lost.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="384" number="151" form="verse" offset="5">This was your motive</line>
<line globalnumber="385" number="152" form="verse">For Paris, was it? Speak.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="386" number="153" form="verse">My lord your son made me to think of this;</line>
<line globalnumber="387" number="154" form="verse">Else Paris, and the medicine, and the King,</line>
<line globalnumber="388" number="155" form="verse">Had from the conversation of my thoughts</line>
<line globalnumber="389" number="156" form="verse" offset="0">Happily been absent then.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="390" number="156" form="verse" offset="5">But think you, Helen,</line>
<line globalnumber="391" number="157" form="verse">If you should tender your supposed aid,</line>
<line globalnumber="392" number="158" form="verse">He would receive it? He and his physicians</line>
<line globalnumber="393" number="159" form="verse">Are of a mind; he, that they cannot help him,</line>
<line globalnumber="394" number="160" form="verse">They, that they cannot help. How shall they credit</line>
<line globalnumber="395" number="161" form="verse">A poor unlearned virgin, when the schools,</line>
<line globalnumber="396" number="162" form="verse">Embowell&#8217;d of their doctrine, have left off</line>
<line globalnumber="397" number="163" form="verse" offset="0">The danger to itself?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="398" number="163" form="verse" offset="4">There&#8217;s something in&#8217;t</line>
<line globalnumber="399" number="164" form="verse">More than my father&#8217;s skill, which was the great&#8217;st</line>
<line globalnumber="400" number="165" form="verse">Of his profession, that his good receipt</line>
<line globalnumber="401" number="166" form="verse">Shall for my legacy be sanctified</line>
<line globalnumber="402" number="167" form="verse">By th&#8217; luckiest stars in heaven, and would your honor</line>
<line globalnumber="403" number="168" form="verse">But give me leave to try success, I&#8217;d venture</line>
<line globalnumber="404" number="169" form="verse">The well-lost life of mine on his Grace&#8217;s cure</line>
<line globalnumber="405" number="170" form="verse" offset="0">By such a day, an hour.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="406" number="170" form="verse" offset="5">Dost thou believe&#8217;t?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="407" number="171" form="verse">Ay, madam, knowingly.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="408" number="172" form="verse">Why, Helen, thou shalt have my leave and love,</line>
<line globalnumber="409" number="173" form="verse">Means and attendants, and my loving greetings</line>
<line globalnumber="410" number="174" form="verse">To those of mine in court. I&#8217;ll stay at home</line>
<line globalnumber="411" number="175" form="verse">And pray God&#8217;s blessing into thy attempt.</line>
<line globalnumber="412" number="176" form="verse">Be gone tomorrow, and be sure of this,</line>
<line globalnumber="413" number="177" form="verse">What I can help thee to thou shalt not miss.</line>
</speech>

<stagedir sdglobalnumber="413.01" sdnumber="177.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>COUNT.</actor>
		<actor>HEL.</actor>
	</action>
</stagedir>

</scene>

</act>

<act num="2">
<acttitle>Act 2</acttitle>

<scene actnum="2" num="1">
<scenetitle>Scene 1</scenetitle>
<scenelocation>Paris. The King&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="KING.">King</scenepersona>
	<scenepersona short="BOTH LORDS.">Lords</scenepersona>
	<scenepersona short="BER.">Bertram Count Roussillon</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
	<scenepersona short="LAF.">Lafew</scenepersona>
	<scenepersona short="HEL.">Helen</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="fr">French</language>
</scenelanguage>


<stagedir sdglobalnumber="413.02" sdnumber="0.01">
	<dir>Enter the King, with diverse young Lords taking leave for the Florentine war, (Bertram) Count Roussillon, and Parolles. Flourish cornets.</dir>
	<action type="enter">
		<actor>KING.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
		<actor>BER.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="414" number="1" form="verse">Farewell, young lords, these warlike principles</line>
<line globalnumber="415" number="2" form="verse">Do not throw from you; and you, my lords, farewell.</line>
<line globalnumber="416" number="3" form="verse">Share the advice betwixt you; if both gain all,</line>
<line globalnumber="417" number="4" form="verse">The gift doth stretch itself as &#8217;tis receiv&#8217;d,</line>
<line globalnumber="418" number="5" form="verse" offset="0">And is enough for both.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="419" number="5" form="verse" offset="5">&#8217;Tis our hope, sir,</line>
<line globalnumber="420" number="6" form="verse">After well-ent&#8217;red soldiers, to return</line>
<line globalnumber="421" number="7" form="verse">And find your Grace in health.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="422" number="8" form="verse">No, no, it cannot be; and yet my heart</line>
<line globalnumber="423" number="9" form="verse">Will not confess he owes the malady</line>
<line globalnumber="424" number="10" form="verse">That doth my life besiege. Farewell, young lords,</line>
<line globalnumber="425" number="11" form="verse">Whether I live or die, be you the sons</line>
<line globalnumber="426" number="12" form="verse">Of worthy Frenchmen. Let higher Italy</line>
<line globalnumber="427" number="13" form="verse">(Those bated that inherit but the fall</line>
<line globalnumber="428" number="14" form="verse">Of the last monarchy) see that you come</line>
<line globalnumber="429" number="15" form="verse">Not to woo honor, but to wed it, when</line>
<line globalnumber="430" number="16" form="verse">The bravest questant shrinks. Find what you seek,</line>
<line globalnumber="431" number="17" form="verse">That fame may cry you loud. I say farewell.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="432" number="18" form="verse">Health, at your bidding, serve your Majesty!</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="433" number="19" form="verse">Those girls of Italy, take heed of them.</line>
<line globalnumber="434" number="20" form="verse">They say our French lack language to deny</line>
<line globalnumber="435" number="21" form="verse">If they demand. Beware of being captives</line>
<line globalnumber="436" number="22" form="verse" offset="0">Before you serve.</line>
</speech>

<speech>
<speaker long="Both French Lords">BOTH LORDS.</speaker>
<line globalnumber="437" number="22" form="verse" offset="4">Our hearts receive your warnings.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="438" number="23" form="verse">Farewell.&#8212;Come hither to me.</line>
</speech>

<stagedir sdglobalnumber="438.01" sdnumber="23.01">
	<dir>The King retires apart with some Lords.</dir>
	<action type="action">
		<actor>KING.</actor>
	</action>
</stagedir>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="439" number="24" form="verse">O my sweet lord, that you will stay behind us!</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="440" number="25" form="verse" offset="0">&#8217;Tis not his fault, the spark.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="441" number="25" form="verse" offset="5">O, &#8217;tis brave wars!</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="442" number="26" form="verse">Most admirable! I have seen those wars.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="443" number="27" form="verse">I am commanded here, and kept a coil with,</line>
<line globalnumber="444" number="28" form="verse">&#8220;Too young&#8221; and &#8220;the next year&#8221; and &#8220;&#8217;tis too early.&#8221;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="445" number="29" form="verse">And thy mind stand to&#8217;t, boy, steal away bravely.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="446" number="30" form="verse">I shall stay here the forehorse to a smock,</line>
<line globalnumber="447" number="31" form="verse">Creaking my shoes on the plain masonry,</line>
<line globalnumber="448" number="32" form="verse">Till honor be bought up, and no sword worn</line>
<line globalnumber="449" number="33" form="verse">But one to dance with! By heaven, I&#8217;ll steal away.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="450" number="34" form="verse" offset="0">There&#8217;s honor in the theft.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="451" number="34" form="verse" offset="5">Commit it, Count.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="452" number="35" form="verse">I am your accessary, and so farewell.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="453" number="36" form="verse">I grow to you, and our parting is a tortur&#8217;d body.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="454" number="37" form="verse">Farewell, captain.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="455" number="38" form="prose">Sweet <foreign xml:lang="fr">Monsieur</foreign> Parolles!</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="456" number="39" form="prose">Noble heroes! My sword and yours are kin. Good sparks and lustrous, a word, good metals: you shall find in the regiment of the Spinii one Captain Spurio, with his cicatrice, an emblem of war, here on his sinister cheek; it was this very sword entrench&#8217;d it. Say to him I live, and observe his reports for me.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="457" number="40" form="prose">We shall, noble captain.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="458" number="41" form="prose">Mars dote on you for his novices!</line>
<stagedir sdglobalnumber="458.01" sdnumber="41.01">
	<dir>Exeunt Lords.</dir>
	<action type="exit">
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="459" number="42" form="prose">What will ye do?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="460" number="43" form="prose">Stay the King.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="461" number="44" form="prose">Use a more spacious ceremony to the noble lords; you have restrain&#8217;d yourself within the list of too cold an <foreign xml:lang="fr">adieu</foreign>. Be more expressive to them, for they wear themselves in the cap of the time, there do muster true gait; eat, speak, and move under the influence of the most receiv&#8217;d star, and though the devil lead the measure, such are to be follow&#8217;d. After them, and take a more dilated farewell.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="462" number="45" form="prose">And I will do so.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="463" number="46" form="prose">Worthy fellows, and like to prove most sinewy swordmen.</line>
</speech>

<stagedir sdglobalnumber="463.01" sdnumber="46.01">
	<dir>Exeunt Bertram and Parolles.</dir>
	<action type="exit">
		<actor>BER.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="463.02" sdnumber="46.02">
	<dir>Enter Lafew.</dir>
	<action type="enter">
		<actor>LAF.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="463.03" sdnumber="46.03">
	<dir>The King comes forward.</dir>
	<action type="action">
		<actor>KING.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<stagedir sdglobalnumber="463.04" sdnumber="46.04">
	<dir>Kneeling.</dir>
	<action type="action">
		<actor>LAF.</actor>
	</action>
</stagedir>
<line globalnumber="464" number="47" form="verse">Pardon, my lord, for me and for my tidings.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="465" number="48" form="verse">I&#8217;ll see thee to stand up.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="466" number="49" form="verse">Then here&#8217;s a man stands that has brought his pardon.</line>
<line globalnumber="467" number="50" form="verse">I would you had kneel&#8217;d, my lord, to ask me mercy,</line>
<line globalnumber="468" number="51" form="verse">And that at my bidding you could so stand up.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="469" number="52" form="verse">I would I had, so I had broke thy pate,</line>
<line globalnumber="470" number="53" form="verse" offset="0">And ask&#8217;d thee mercy for&#8217;t.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="471" number="53" form="verse" offset="5">Good faith, across!</line>
<line globalnumber="472" number="54" form="verse">But, my good lord, &#8217;tis thus: will you be cur&#8217;d</line>
<line globalnumber="473" number="55" form="verse" offset="0">Of your infirmity?</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="474" number="55" form="verse" offset="5">No.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="475" number="55" form="verse" offset="6">O, will you eat</line>
<line globalnumber="476" number="56" form="verse">No grapes, my royal fox? Yes, but you will</line>
<line globalnumber="477" number="57" form="verse">My noble grapes, and if my royal fox</line>
<line globalnumber="478" number="58" form="verse">Could reach them. I have seen a medicine</line>
<line globalnumber="479" number="59" form="verse">That&#8217;s able to breathe life into a stone,</line>
<line globalnumber="480" number="60" form="verse">Quicken a rock, and make you dance canary</line>
<line globalnumber="481" number="61" form="verse">With spritely fire and motion, whose simple touch</line>
<line globalnumber="482" number="62" form="verse">Is powerful to araise King
Pippen, nay,</line>
<line globalnumber="483" number="63" form="verse">To give great Charlemain a pen in &#8217;s hand</line>
<line globalnumber="484" number="64" form="verse" offset="0">And write to her a love-line.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="485" number="64" form="verse" offset="6">What her is this?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="486" number="65" form="verse">Why, Doctor She! My lord, there&#8217;s one arriv&#8217;d,</line>
<line globalnumber="487" number="66" form="verse">If you will see her. Now by my faith and honor,</line>
<line globalnumber="488" number="67" form="verse">If seriously I may convey my thoughts</line>
<line globalnumber="489" number="68" form="verse">In this my light deliverance, I have spoke</line>
<line globalnumber="490" number="69" form="verse">With one, that in her sex, her years, profession,</line>
<line globalnumber="491" number="70" form="verse">Wisdom, and constancy, hath amaz&#8217;d me more</line>
<line globalnumber="492" number="71" form="verse">Than I dare blame my weakness. Will you see her&#8212;</line>
<line globalnumber="493" number="72" form="verse">For that is her demand&#8212;and know her business?</line>
<line globalnumber="494" number="73" form="verse" offset="0">That done, laugh well at me.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="495" number="73" form="verse" offset="6">Now, good Lafew,</line>
<line globalnumber="496" number="74" form="verse">Bring in the admiration, that we with thee</line>
<line globalnumber="497" number="75" form="verse">May spend our wonder too, or take off thine</line>
<line globalnumber="498" number="76" form="verse" offset="0">By wond&#8217;ring how thou took&#8217;st it.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="499" number="76" form="verse" offset="7">Nay, I&#8217;ll fit you,</line>
<line globalnumber="500" number="77" form="verse">And not be all day neither.</line>
</speech>

<stagedir sdglobalnumber="500.01" sdnumber="77.01">
	<dir>Goes to the door.</dir>
	<action type="action">
		<actor>LAF.</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="501" number="78" form="verse">Thus he his special nothing ever prologues.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="502" number="79" form="verse" offset="0">Nay, come your ways.</line>
</speech>

<stagedir sdglobalnumber="502.01" sdnumber="79.01">
	<dir>Enter Helen.</dir>
	<action type="enter">
		<actor>HEL.</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="503" number="79" form="verse" offset="5">This haste hath wings indeed.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="504" number="80" form="verse">Nay, come your ways;</line>
<line globalnumber="505" number="81" form="verse">This is his Majesty, say your mind to him.</line>
<line globalnumber="506" number="82" form="verse">A traitor you do look like, but such traitors</line>
<line globalnumber="507" number="83" form="verse">His Majesty seldom fears. I am Cressid&#8217;s uncle,</line>
<line globalnumber="508" number="84" form="verse">That dare leave two together; fare you well.</line>
</speech>

<stagedir sdglobalnumber="508.01" sdnumber="84.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>LAF.</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="509" number="85" form="verse">Now, fair one, does your business follow us?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="510" number="86" form="verse">Ay, my good lord.</line>
<line globalnumber="511" number="87" form="verse">Gerard de Narbon was my father,</line>
<line globalnumber="512" number="88" form="verse" offset="0">In what he did profess, well found.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="513" number="88" form="verse" offset="7">I knew him.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="514" number="89" form="verse">The rather will I spare my praises towards him,</line>
<line globalnumber="515" number="90" form="verse">Knowing him is enough. On &#8217;s bed of death</line>
<line globalnumber="516" number="91" form="verse">Many receipts he gave me; chiefly one,</line>
<line globalnumber="517" number="92" form="verse">Which as the dearest issue of his practice,</line>
<line globalnumber="518" number="93" form="verse">And of his old experience th&#8217; only darling,</line>
<line globalnumber="519" number="94" form="verse">He bade me store up, as a triple eye,</line>
<line globalnumber="520" number="95" form="verse">Safer than mine own two, more dear. I have so,</line>
<line globalnumber="521" number="96" form="verse">And hearing your high Majesty is touch&#8217;d</line>
<line globalnumber="522" number="97" form="verse">With that malignant cause wherein the honor</line>
<line globalnumber="523" number="98" form="verse">Of my dear father&#8217;s gift stands chief in power,</line>
<line globalnumber="524" number="99" form="verse">I come to tender it, and my appliance,</line>
<line globalnumber="525" number="100" form="verse" offset="0">With all bound humbleness.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="526" number="100" form="verse" offset="6">We thank you, maiden,</line>
<line globalnumber="527" number="101" form="verse">But may not be so credulous of cure,</line>
<line globalnumber="528" number="102" form="verse">When our most learned doctors leave us, and</line>
<line globalnumber="529" number="103" form="verse">The congregated college have concluded</line>
<line globalnumber="530" number="104" form="verse">That laboring art can never ransom nature</line>
<line globalnumber="531" number="105" form="verse">From her inaidible estate; I say we must not</line>
<line globalnumber="532" number="106" form="verse">So stain our judgment, or corrupt our hope,</line>
<line globalnumber="533" number="107" form="verse">To prostitute our past-cure malady</line>
<line globalnumber="534" number="108" form="verse">To empirics, or to dissever so</line>
<line globalnumber="535" number="109" form="verse">Our great self and our credit, to esteem</line>
<line globalnumber="536" number="110" form="verse">A senseless help when help past sense we deem.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="537" number="111" form="verse">My duty then shall pay me for my pains.</line>
<line globalnumber="538" number="112" form="verse">I will no more enforce mine office on you,</line>
<line globalnumber="539" number="113" form="verse">Humbly entreating from your royal thoughts</line>
<line globalnumber="540" number="114" form="verse">A modest one, to bear me back again.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="541" number="115" form="verse">I cannot give thee less, to be call&#8217;d grateful.</line>
<line globalnumber="542" number="116" form="verse">Thou thought&#8217;st to help me, and such thanks I give</line>
<line globalnumber="543" number="117" form="verse">As one near death to those that wish him live.</line>
<line globalnumber="544" number="118" form="verse">But what at full I know, thou know&#8217;st no part,</line>
<line globalnumber="545" number="119" form="verse">I knowing all my peril, thou no art.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="546" number="120" form="verse">What I can do can do no hurt to try,</line>
<line globalnumber="547" number="121" form="verse">Since you set up your rest &#8217;gainst remedy.</line>
<line globalnumber="548" number="122" form="verse">He that of greatest works is finisher</line>
<line globalnumber="549" number="123" form="verse">Oft does them by the weakest minister:</line>
<line globalnumber="550" number="124" form="verse">So holy writ in babes hath judgment shown,</line>
<line globalnumber="551" number="125" form="verse">When judges have been babes; great floods have flown</line>
<line globalnumber="552" number="126" form="verse">From simple sources; and great seas have dried</line>
<line globalnumber="553" number="127" form="verse">When miracles have by the great&#8217;st been denied.</line>
<line globalnumber="554" number="128" form="verse">Oft expectation fails, and most oft there</line>
<line globalnumber="555" number="129" form="verse">Where most it promises; and oft it hits</line>
<line globalnumber="556" number="130" form="verse">Where hope is coldest, and despair most fits.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="557" number="131" form="verse">I must not hear thee; fare thee well, kind maid,</line>
<line globalnumber="558" number="132" form="verse">Thy pains not us&#8217;d must by thyself be paid.</line>
<line globalnumber="559" number="133" form="verse">Proffers not took reap thanks for their reward.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="560" number="134" form="verse">Inspired merit so by breath is barr&#8217;d.</line>
<line globalnumber="561" number="135" form="verse">It is not so with Him that all things knows</line>
<line globalnumber="562" number="136" form="verse">As &#8217;tis with us that square our guess by shows;</line>
<line globalnumber="563" number="137" form="verse">But most it is presumption in us when</line>
<line globalnumber="564" number="138" form="verse">The help of heaven we count the act of men.</line>
<line globalnumber="565" number="139" form="verse">Dear sir, to my endeavors give consent,</line>
<line globalnumber="566" number="140" form="verse">Of heaven, not me, make an experiment.</line>
<line globalnumber="567" number="141" form="verse">I am not an imposture that proclaim</line>
<line globalnumber="568" number="142" form="verse">Myself against the level of mine aim,</line>
<line globalnumber="569" number="143" form="verse">But know I think, and think I know most sure,</line>
<line globalnumber="570" number="144" form="verse">My art is not past power, nor you past cure.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="571" number="145" form="verse">Art thou so confident? Within what space</line>
<line globalnumber="572" number="146" form="verse" offset="0">Hop&#8217;st thou my cure?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="573" number="146" form="verse" offset="4">The greatest grace lending grace,</line>
<line globalnumber="574" number="147" form="verse">Ere twice the horses of the sun shall bring</line>
<line globalnumber="575" number="148" form="verse">Their fiery torcher his diurnal ring,</line>
<line globalnumber="576" number="149" form="verse">Ere twice in murk and occidental damp</line>
<line globalnumber="577" number="150" form="verse">Moist Hesperus hath quench&#8217;d her sleepy lamp,</line>
<line globalnumber="578" number="151" form="verse">Or four and twenty times the pilot&#8217;s glass</line>
<line globalnumber="579" number="152" form="verse">Hath told the thievish minutes how they pass,</line>
<line globalnumber="580" number="153" form="verse">What is infirm from your sound parts shall fly,</line>
<line globalnumber="581" number="154" form="verse">Health shall live free, and sickness freely die.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="582" number="155" form="verse">Upon thy certainty and confidence</line>
<line globalnumber="583" number="156" form="verse" offset="0">What dar&#8217;st thou venter?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="584" number="156" form="verse" offset="5">Tax of impudence,</line>
<line globalnumber="585" number="157" form="verse">A strumpet&#8217;s boldness, a divulged shame,</line>
<line globalnumber="586" number="158" form="verse">Traduc&#8217;d by odious ballads; my maiden&#8217;s name</line>
<line globalnumber="587" number="159" form="verse">Sear&#8217;d otherwise; ne worse of worst&#8212;extended</line>
<line globalnumber="588" number="160" form="verse">With vildest torture, let my life be ended.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="589" number="161" form="verse">Methinks in thee some blessed spirit doth speak</line>
<line globalnumber="590" number="162" form="verse">His powerful sound within an organ weak;</line>
<line globalnumber="591" number="163" form="verse">And what impossibility would slay</line>
<line globalnumber="592" number="164" form="verse">In common sense, sense saves another way.</line>
<line globalnumber="593" number="165" form="verse">Thy life is dear, for all that life can rate</line>
<line globalnumber="594" number="166" form="verse">Worth name of life in thee hath estimate:</line>
<line globalnumber="595" number="167" form="verse">Youth, beauty, wisdom, courage, all</line>
<line globalnumber="596" number="168" form="verse">That happiness and prime can happy call.</line>
<line globalnumber="597" number="169" form="verse">Thou this to hazard needs must intimate</line>
<line globalnumber="598" number="170" form="verse">Skill infinite, or monstrous desperate.</line>
<line globalnumber="599" number="171" form="verse">Sweet practicer, thy physic I will try,</line>
<line globalnumber="600" number="172" form="verse">That ministers thine own death if I die.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="601" number="173" form="verse">If I break time, or flinch in property</line>
<line globalnumber="602" number="174" form="verse">Of what I spoke, unpitied let me die,</line>
<line globalnumber="603" number="175" form="verse">And well deserv&#8217;d. Not helping, death&#8217;s my fee,</line>
<line globalnumber="604" number="176" form="verse">But if I help, what do you promise me?</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="605" number="177" form="verse" offset="0">Make thy demand.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="606" number="177" form="verse" offset="4">But will you make it even?</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="607" number="178" form="verse">Ay, by my sceptre and my hopes of heaven.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="608" number="179" form="verse">Then shalt thou give me with thy kingly hand</line>
<line globalnumber="609" number="180" form="verse">What husband in thy power I will command.</line>
<line globalnumber="610" number="181" form="verse">Exempted be from me the arrogance</line>
<line globalnumber="611" number="182" form="verse">To choose from forth the royal blood of France,</line>
<line globalnumber="612" number="183" form="verse">My low and humble name to propagate</line>
<line globalnumber="613" number="184" form="verse">With any branch or image of thy state;</line>
<line globalnumber="614" number="185" form="verse">But such a one thy vassal, whom I know</line>
<line globalnumber="615" number="186" form="verse">Is free for me to ask, thee to bestow.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="616" number="187" form="verse">Here is my hand, the premises observ&#8217;d,</line>
<line globalnumber="617" number="188" form="verse">Thy will by my performance shall be serv&#8217;d.</line>
<line globalnumber="618" number="189" form="verse">So make the choice of thy own time, for I,</line>
<line globalnumber="619" number="190" form="verse">Thy resolv&#8217;d patient, on thee still rely.</line>
<line globalnumber="620" number="191" form="verse">More should I question thee, and more I must&#8212;</line>
<line globalnumber="621" number="192" form="verse">Though more to know could not be more to trust&#8212;</line>
<line globalnumber="622" number="193" form="verse">From whence thou cam&#8217;st, how tended on, but rest</line>
<line globalnumber="623" number="194" form="verse">Unquestion&#8217;d welcome and undoubted blest.&#8212;</line>
<line globalnumber="624" number="195" form="verse">Give me some help here ho!&#8212;If thou proceed</line>
<line globalnumber="625" number="196" form="verse">As high as word, my deed shall match thy deed.</line>
</speech>

<stagedir sdglobalnumber="625.01" sdnumber="196.01">
	<dir>Flourish. Exeunt.</dir>
	<action type="exit">
		<actor>KING.</actor>
		<actor>HEL.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="2" num="2">
<scenetitle>Scene 2</scenetitle>
<scenelocation>Roussillon. The Count&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="COUNT.">Countess</scenepersona>
	<scenepersona short="CLO.">Clown</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="625.02" sdnumber="0.01">
	<dir>Enter Countess and Clown.</dir>
	<action type="enter">
		<actor>COUNT.</actor>
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="626" number="1" form="prose">Come on, sir, I shall now put you to the height of your breeding.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="627" number="2" form="prose">I will show myself highly fed and lowly taught. I know my business is but to the court.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="628" number="3" form="prose">To the court! Why, what place make you special, when you put off that with such contempt? But to the court!</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="629" number="4" form="prose">Truly, madam, if God have lent a man any manners, he may easily put it off at court. He that cannot make a leg, put off &#8217;s cap, kiss his hand, and say nothing, has neither leg, hands, lip, nor cap; and indeed such a fellow, to say precisely, were not for the court; but for me, I have an answer will serve all men.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="630" number="5" form="prose">Marry, that&#8217;s a bountiful answer that fits all questions.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="631" number="6" form="prose">It is like a barber&#8217;s chair that fits all buttocks: the pin-buttock, the quatch-buttock, the brawn-buttock, or any buttock.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="632" number="7" form="prose">Will your answer serve fit to all questions?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="633" number="8" form="prose">As fit as ten groats is for the hand of an attorney, as your French crown for your taffety punk, as Tib&#8217;s rush for Tom&#8217;s forefinger, as a pancake for <date type="holiday" subtype="Christian">Shrove Tuesday</date>, a morris for <date type="holiday" subtype="Roman">May-day</date>, as the nail to his hole, the cuckold to his horn, as a scolding quean to a wrangling knave, as the nun&#8217;s lip to the friar&#8217;s mouth, nay, as the pudding to his skin.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="634" number="9" form="prose">Have you, I say, an answer of such fitness for all questions?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="635" number="10" form="prose">From below your duke to beneath your constable, it will fit any question.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="636" number="11" form="prose">It must be an answer of most monstrous size that must fit all demands.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="637" number="12" form="prose">But a trifle neither, in good faith, if the learned should speak truth of it. Here it is, and all that belongs to&#8217;t. Ask me if I am a courtier: it shall do you no harm to learn.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="638" number="13" form="prose">To be young again, if we could, I will be a fool in question, hoping to be the wiser by your answer. I pray you, sir, are you a courtier?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="639" number="14" form="prose">O Lord, sir!&#8212;There&#8217;s a simple putting off. More, more, a hundred of them.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="640" number="15" form="prose">Sir, I am a poor friend of yours that loves you.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="641" number="16" form="prose">O Lord, sir!&#8212;Thick, thick, spare not me.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="642" number="17" form="prose">I think, sir, you can eat none of this homely meat.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="643" number="18" form="prose">O Lord, sir!&#8212;Nay, put me to&#8217;t, I warrant you.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="644" number="19" form="prose">You were lately whipt, sir, as I think.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="645" number="20" form="prose">O Lord, sir!&#8212;Spare not me.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="646" number="21" form="prose">Do you cry, &#8220;O Lord, sir!&#8221; at your whipping, and &#8220;Spare not me&#8221;? Indeed your &#8220;O Lord, sir!&#8221; is very sequent to your whipping; you would answer very well to a whipping, if you were but bound to&#8217;t.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="647" number="22" form="prose">I ne&#8217;er had worse luck in my life in my &#8220;O Lord, sir!&#8221; I see things may serve long, but not serve ever.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="648" number="23" form="verse">I play the noble huswife with the time,</line>
<line globalnumber="649" number="24" form="verse">To entertain it so merrily with a fool.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="650" number="25" form="verse">O Lord, sir!&#8212;Why, there&#8217;t serves well again.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="651" number="26" form="verse">An end, sir; to your business: give Helen this,</line>
<line globalnumber="652" number="27" form="verse">And urge her to a present answer back.</line>
<line globalnumber="653" number="28" form="verse">Commend me to my kinsmen and my son.</line>
<line globalnumber="654" number="29" form="verse">This is not much.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="655" number="30" form="prose">Not much commendation to them.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="656" number="31" form="prose">Not much employment for you. You understand me?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="657" number="32" form="prose">Most fruitfully, I am there before my legs.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="658" number="33" form="prose">Haste you again.</line>
</speech>

<stagedir sdglobalnumber="658.01" sdnumber="33.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>COUNT.</actor>
		<actor>CLO.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="2" num="3">
<scenetitle>Scene 3</scenetitle>
<scenelocation>Paris. The King&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="BER.">Bertram</scenepersona>
	<scenepersona short="LAF.">Lafew</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
	<scenepersona short="KING.">King</scenepersona>
	<scenepersona short="HEL.">Helen</scenepersona>
	<scenepersona>Attendants</scenepersona>
	<scenepersona short="BOTH LORDS.">Lords</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="fr">French</language>
    <language short="it">Italian</language>
    <language short="nl">Dutch</language>
</scenelanguage>


<stagedir sdglobalnumber="658.02" sdnumber="0.01">
	<dir>Enter count Bertram, Lafew, and Parolles.</dir>
	<action type="enter">
		<actor>BER.</actor>
		<actor>LAF.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="659" number="1" form="prose">They say miracles are past, and we have our philosophical persons, to make modern and familiar, things supernatural and causeless. Hence is it that we make trifles of terrors, ensconcing ourselves into seeming knowledge, when we should submit ourselves to an unknown fear.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="660" number="2" form="prose">Why, &#8217;tis the rarest argument of wonder that hath shot out in our latter times.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="661" number="3" form="prose">And so &#8217;tis.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="662" number="4" form="prose">To be relinquish&#8217;d of the artists&#8212;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="663" number="5" form="prose">So I say, both of Galen and Paracelsus.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="664" number="6" form="prose">Of all the learned and authentic fellows&#8212;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="665" number="7" form="prose">Right, so I say.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="666" number="8" form="prose">That gave him out incurable&#8212;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="667" number="9" form="prose">Why, there &#8217;tis, so say I too.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="668" number="10" form="prose">Not to be help&#8217;d&#8212;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="669" number="11" form="prose">Right, as &#8217;twere a man assur&#8217;d of a&#8212;</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="670" number="12" form="prose">Uncertain life, and sure death.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="671" number="13" form="prose">Just, you say well; so would I have said.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="672" number="14" form="prose">I may truly say it is a novelty to the world.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="673" number="15" form="prose">It is indeed; if you will have it in showing, you shall read it in what-do-ye-call there.</line>
</speech>

<stagedir sdglobalnumber="673.01" sdnumber="15.01">
	<dir>Pointing to a ballad in Lafew&#8217;s hand.</dir>
	<action type="action">
		<actor>PAR.</actor>
		<recipient>LAF.</recipient>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<stagedir sdglobalnumber="673.02" sdnumber="15.02">
	<dir>Reading the title.</dir>
	<action type="read">
		<actor>LAF.</actor>
	</action>
</stagedir>
<line globalnumber="674" number="16" form="prose"><recite>&#8220;A showing of a heavenly effect in an earthly actor.&#8221;</recite></line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="675" number="17" form="prose">That&#8217;s it I would have said, the very same.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="676" number="18" form="prose">Why, your dolphin is not lustier. &#8217;Fore me, I speak in respect&#8212;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="677" number="19" form="prose">Nay, &#8217;tis strange, &#8217;tis very strange, that is the brief and the tedious of it, and he&#8217;s of a most facinerious spirit that will not acknowledge it to be the&#8212;</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="678" number="20" form="prose">Very hand of heaven.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="679" number="21" form="prose">Ay, so I say.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="680" number="22" form="prose">In a most weak&#8212;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="681" number="23" form="prose">And debile minister, great power, great transcendence, which should indeed give us a further use to be made than alone the recov&#8217;ry of the King, as to be&#8212;</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="682" number="24" form="prose">Generally thankful.</line>
</speech>

<stagedir sdglobalnumber="682.01" sdnumber="24.01">
	<dir>Enter King, Helen, and Attendants.</dir>
	<action type="enter">
		<actor>KING.</actor>
		<actor>HEL.</actor>
		<actor>Attendants</actor>
	</action>
</stagedir>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="683" number="25" form="prose">I would have said it; you say well. Here comes the King.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="684" number="26" form="prose"><foreign xml:lang="nl">Lustig</foreign>, as the Dutchman says. I&#8217;ll like a maid the better whilst I have a tooth in my head. Why, he&#8217;s able to lead her a <foreign xml:lang="fr">coranto</foreign>.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="685" number="27" form="prose"><foreign xml:lang="fr">Mort du vinaigre!</foreign> Is not this Helen?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="686" number="28" form="prose">&#8217;Fore God, I think so.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="687" number="29" form="verse">Go call before me all the lords in court.</line>
<line globalnumber="688" number="30" form="verse">Sit, my preserver, by thy patient&#8217;s side,</line>
<line globalnumber="689" number="31" form="verse">And with this healthful hand, whose banish&#8217;d sense</line>
<line globalnumber="690" number="32" form="verse">Thou hast repeal&#8217;d, a second time receive</line>
<line globalnumber="691" number="33" form="verse">The confirmation of my promis&#8217;d gift,</line>
<line globalnumber="692" number="34" form="verse">Which but attends thy naming.</line>
<stagedir sdglobalnumber="692.01" sdnumber="34.01">
	<dir>Enter three or four Lords.</dir>
	<action type="enter">
		<actor>1. LORD.</actor>
		<actor>2. LORD.</actor>
		<actor>3. LORD.</actor>
		<actor>4. LORD.</actor>
	</action>
</stagedir>
<line globalnumber="693" number="35" form="verse">Fair maid, send forth thine eye. This youthful parcel</line>
<line globalnumber="694" number="36" form="verse">Of noble bachelors stand at my bestowing,</line>
<line globalnumber="695" number="37" form="verse">O&#8217;er whom both sovereign power and father&#8217;s voice</line>
<line globalnumber="696" number="38" form="verse">I have to use. Thy frank election make;</line>
<line globalnumber="697" number="39" form="verse">Thou hast power to choose, and they none to forsake.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="698" number="40" form="verse">To each of you one fair and virtuous mistress</line>
<line globalnumber="699" number="41" form="verse">Fall, when Love please! Marry, to each but one!</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="700" number="42" form="verse">I&#8217;d give bay Curtal and his furniture,</line>
<line globalnumber="701" number="43" form="verse">My mouth no more were broken than these boys&#8217;,</line>
<line globalnumber="702" number="44" form="verse" offset="0">And writ as little beard.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="703" number="44" form="verse" offset="5">Peruse them well.</line>
<line globalnumber="704" number="45" form="verse">Not one of those but had a noble father.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="705" number="46" form="verse">Gentlemen,</line>
<line globalnumber="706" number="47" form="verse">Heaven hath through me restor&#8217;d the King to health.</line>
</speech>

<speech>
<speaker long="All French Lords">ALL LORDS.</speaker>
<line globalnumber="707" number="48" form="verse">We understand it, and thank heaven for you.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="708" number="49" form="verse">I am a simple maid, and therein wealthiest</line>
<line globalnumber="709" number="50" form="verse">That I protest I simply am a maid.</line>
<line globalnumber="710" number="51" form="verse">Please it your Majesty, I have done already.</line>
<line globalnumber="711" number="52" form="verse">The blushes in my cheeks thus whisper me,</line>
<line globalnumber="712" number="53" form="verse">&#8220;We blush that thou shouldst choose; but be refused,</line>
<line globalnumber="713" number="54" form="verse">Let the white death sit on thy cheek forever,</line>
<line globalnumber="714" number="55" form="verse" offset="0">We&#8217;ll ne&#8217;er come there again.&#8221;</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="715" number="55" form="verse" offset="6">Make choice and see,</line>
<line globalnumber="716" number="56" form="verse">Who shuns thy love shuns all his love in me.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="717" number="57" form="verse">Now, Dian, from thy altar do I fly,</line>
<line globalnumber="718" number="58" form="verse">And to imperial Love, that god most high,</line>
<line globalnumber="719" number="59" form="verse">Do my sighs stream.</line>
<stagedir sdglobalnumber="719.01" sdnumber="59.01">
	<dir>She addresses her to a Lord.</dir>
	<action type="action">
		<actor>HEL.</actor>
		<recipient>1. LORD.</recipient>
	</action>
</stagedir>
<line globalnumber="720" number="60" form="verse">Sir, will you hear my suit?</line>
</speech>

<speech>
<speaker long="First French Lord">1. LORD.</speaker>
<line globalnumber="721" number="61" form="verse" offset="0">And grant it.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="722" number="61" form="verse" offset="3">Thanks, sir; all the rest is mute.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="723" number="62" form="prose">I had rather be in this choice than throw ames-ace for my life.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<stagedir sdglobalnumber="723.01" sdnumber="62.01">
	<dir>To a Second Lord.</dir>
	<action type="speak">
		<actor>HEL.</actor>
		<recipient>2. LORD.</recipient>
	</action>
</stagedir>
<line globalnumber="724" number="63" form="verse">The honor, sir, that flames in your fair eyes,</line>
<line globalnumber="725" number="64" form="verse">Before I speak, too threat&#8217;ningly replies.</line>
<line globalnumber="726" number="65" form="verse">Love make your fortunes twenty times above</line>
<line globalnumber="727" number="66" form="verse">Her that so wishes, and her humble love!</line>
</speech>

<speech>
<speaker long="Second French Lord">2. LORD.</speaker>
<line globalnumber="728" number="67" form="verse" offset="0">No better, if you please.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="729" number="67" form="verse" offset="5">My wish receive,</line>
<line globalnumber="730" number="68" form="verse">Which great Love grant, and so I take my leave.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="731" number="69" form="prose">Do all they deny her? And they were sons of mine, I&#8217;d have them whipt, or I would send them to th&#8217; Turk to make eunuchs of.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>

<stagedir sdglobalnumber="731.01" sdnumber="69.01">
	<dir>To a third Lord.</dir>
	<action type="speak">
		<actor>HEL.</actor>
		<recipient>3. LORD.</recipient>
	</action>
</stagedir>
<line globalnumber="732" number="70" form="verse">Be not afraid that I your hand should take,</line>
<line globalnumber="733" number="71" form="verse">I&#8217;ll never do you wrong for your own sake.</line>
<line globalnumber="734" number="72" form="verse">Blessing upon your vows, and in your bed</line>
<line globalnumber="735" number="73" form="verse">Find fairer fortune, if you ever wed!</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="736" number="74" form="prose">These boys are boys of ice, they&#8217;ll none have her. Sure they are bastards to the English, the French ne&#8217;er got &#8217;em.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<stagedir sdglobalnumber="736.01" sdnumber="74.01">
	<dir>To a fourth Lord.</dir>
	<action type="speak">
		<actor>HEL.</actor>
		<recipient>4. LORD.</recipient>
	</action>
</stagedir>
<line globalnumber="737" number="75" form="verse">You are too young, too happy, and too good,</line>
<line globalnumber="738" number="76" form="verse">To make yourself a son out of my blood.</line>
</speech>

<speech>
<speaker long="Fourth French Lord">4. LORD.</speaker>
<line globalnumber="739" number="77" form="verse">Fair one, I think not so.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="740" number="78" form="prose">There&#8217;s one grape yet; I am sure thy father drunk wine&#8212;but if thou be&#8217;st not an ass, I am a youth of fourteen. I have known thee already.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>

<stagedir sdglobalnumber="740.01" sdnumber="78.01">
	<dir>To Bertram.</dir>
	<action type="speak">
		<actor>HEL.</actor>
		<recipient>BER.</recipient>
	</action>
</stagedir>
<line globalnumber="741" number="79" form="verse">I dare not say I take you, but I give</line>
<line globalnumber="742" number="80" form="verse">Me and my service, ever whilst I live,</line>
<line globalnumber="743" number="81" form="verse">Into your guiding power.&#8212;This is the man.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="744" number="82" form="verse">Why then, young Bertram, take her, she&#8217;s thy wife.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="745" number="83" form="verse">My wife, my liege? I shall beseech your Highness,</line>
<line globalnumber="746" number="84" form="verse">In such a business, give me leave to use</line>
<line globalnumber="747" number="85" form="verse" offset="0">The help of mine own eyes.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="748" number="85" form="verse" offset="5">Know&#8217;st thou not, Bertram,</line>
<line globalnumber="749" number="86" form="verse">What she has done for me?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="750" number="87" form="verse">Yes, my good lord,</line>
<line globalnumber="751" number="88" form="verse">But never hope to know why I should marry her.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="752" number="89" form="verse">Thou know&#8217;st she has rais&#8217;d me from my sickly bed.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="753" number="90" form="verse">But follows it, my lord, to bring me down</line>
<line globalnumber="754" number="91" form="verse">Must answer for your raising? I know her well;</line>
<line globalnumber="755" number="92" form="verse">She had her breeding at my father&#8217;s charge&#8212;</line>
<line globalnumber="756" number="93" form="verse">A poor physician&#8217;s daughter my wife! Disdain</line>
<line globalnumber="757" number="94" form="verse">Rather corrupt me ever!</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="758" number="95" form="verse">&#8217;Tis only title thou disdain&#8217;st in her, the which</line>
<line globalnumber="759" number="96" form="verse">I can build up. Strange is it that our bloods,</line>
<line globalnumber="760" number="97" form="verse">Of color, weight, and heat, pour&#8217;d all together,</line>
<line globalnumber="761" number="98" form="verse">Would quite confound distinction, yet stands off</line>
<line globalnumber="762" number="99" form="verse">In differences so mighty. If she be</line>
<line globalnumber="763" number="100" form="verse">All that is virtuous&#8212;save what thou dislik&#8217;st,</line>
<line globalnumber="764" number="101" form="verse">A poor physician&#8217;s daughter&#8212;thou dislik&#8217;st</line>
<line globalnumber="765" number="102" form="verse">Of virtue for the name. But do not so.</line>
<line globalnumber="766" number="103" form="verse">From lowest place when virtuous things proceed,</line>
<line globalnumber="767" number="104" form="verse">The place is dignified by th&#8217; doer&#8217;s deed.</line>
<line globalnumber="768" number="105" form="verse">Where great additions swell &#8217;s, and virtue none,</line>
<line globalnumber="769" number="106" form="verse">It is a dropsied honor. Good alone</line>
<line globalnumber="770" number="107" form="verse">Is good, without a name; vileness is so:</line>
<line globalnumber="771" number="108" form="verse">The property by what it is should go,</line>
<line globalnumber="772" number="109" form="verse">Not by the title. She is young, wise, fair,</line>
<line globalnumber="773" number="110" form="verse">In these to nature she&#8217;s immediate heir;</line>
<line globalnumber="774" number="111" form="verse">And these breed honor. That is honor&#8217;s scorn,</line>
<line globalnumber="775" number="112" form="verse">Which challenges itself as honor&#8217;s born,</line>
<line globalnumber="776" number="113" form="verse">And is not like the sire. Honors thrive,</line>
<line globalnumber="777" number="114" form="verse">When rather from our acts we them derive</line>
<line globalnumber="778" number="115" form="verse">Than our foregoers. The mere word&#8217;s a slave</line>
<line globalnumber="779" number="116" form="verse">Debosh&#8217;d on every tomb, on every grave</line>
<line globalnumber="780" number="117" form="verse">A lying trophy, and as oft is dumb</line>
<line globalnumber="781" number="118" form="verse">Where dust and damn&#8217;d oblivion is the tomb</line>
<line globalnumber="782" number="119" form="verse">Of honor&#8217;d bones indeed. What should be said?</line>
<line globalnumber="783" number="120" form="verse">If thou canst like this creature as a maid,</line>
<line globalnumber="784" number="121" form="verse">I can create the rest. Virtue and she</line>
<line globalnumber="785" number="122" form="verse">Is her own dower; honor and wealth from me.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="786" number="123" form="verse">I cannot love her, nor will strive to do&#8217;t.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="787" number="124" form="verse">Thou wrong&#8217;st thyself, if thou shouldst strive to choose.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="788" number="125" form="verse">That you are well restor&#8217;d, my lord, I&#8217;m glad.</line>
<line globalnumber="789" number="126" form="verse">Let the rest go.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="790" number="127" form="verse">My honor&#8217;s at the stake, which to defeat,</line>
<line globalnumber="791" number="128" form="verse">I must produce my power. Here, take her hand,</line>
<line globalnumber="792" number="129" form="verse">Proud scornful boy, unworthy this good gift,</line>
<line globalnumber="793" number="130" form="verse">That dost in vile misprision shackle up</line>
<line globalnumber="794" number="131" form="verse">My love and her desert; that canst not dream,</line>
<line globalnumber="795" number="132" form="verse">We poising us in her defective scale,</line>
<line globalnumber="796" number="133" form="verse">Shall weigh thee to the beam; that wilt not know</line>
<line globalnumber="797" number="134" form="verse">It is in us to plant thine honor where</line>
<line globalnumber="798" number="135" form="verse">We please to have it grow. Check thy contempt;</line>
<line globalnumber="799" number="136" form="verse">Obey our will, which travails in thy good;</line>
<line globalnumber="800" number="137" form="verse">Believe not thy disdain, but presently</line>
<line globalnumber="801" number="138" form="verse">Do thine own fortunes that obedient right</line>
<line globalnumber="802" number="139" form="verse">Which both thy duty owes and our power claims,</line>
<line globalnumber="803" number="140" form="verse">Or I will throw thee from my care forever</line>
<line globalnumber="804" number="141" form="verse">Into the staggers and the careless lapse</line>
<line globalnumber="805" number="142" form="verse">Of youth and ignorance; both my revenge and hate</line>
<line globalnumber="806" number="143" form="verse">Loosing upon thee, in the name of justice,</line>
<line globalnumber="807" number="144" form="verse">Without all terms of pity. Speak, thine answer.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="808" number="145" form="verse">Pardon, my gracious lord; for I submit</line>
<line globalnumber="809" number="146" form="verse">My fancy to your eyes. When I consider</line>
<line globalnumber="810" number="147" form="verse">What great creation and what dole of honor</line>
<line globalnumber="811" number="148" form="verse">Flies where you bid it, I find that she, which late</line>
<line globalnumber="812" number="149" form="verse">Was in my nobler thoughts most base, is now</line>
<line globalnumber="813" number="150" form="verse">The praised of the King, who so ennobled,</line>
<line globalnumber="814" number="151" form="verse" offset="0">Is as &#8217;twere born so.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="815" number="151" form="verse" offset="4">Take her by the hand,</line>
<line globalnumber="816" number="152" form="verse">And tell her she is thine; to whom I promise</line>
<line globalnumber="817" number="153" form="verse">A counterpoise&#8212;if not to thy estate</line>
<line globalnumber="818" number="154" form="verse" offset="0">A balance more replete.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="819" number="154" form="verse" offset="5">I take her hand.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="820" number="155" form="verse">Good fortune and the favor of the King</line>
<line globalnumber="821" number="156" form="verse">Smile upon this contract, whose ceremony</line>
<line globalnumber="822" number="157" form="verse">Shall seem expedient on the now-born brief,</line>
<line globalnumber="823" number="158" form="verse">And be perform&#8217;d tonight. The solemn feast</line>
<line globalnumber="824" number="159" form="verse">Shall more attend upon the coming space,</line>
<line globalnumber="825" number="160" form="verse">Expecting absent friends. As thou lov&#8217;st her,</line>
<line globalnumber="826" number="161" form="verse">Thy love&#8217;s to me religious; else, does err.</line>
</speech>

<stagedir sdglobalnumber="826.01" sdnumber="161.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>KING.</actor>
		<actor>BER.</actor>
		<actor>HEL.</actor>
		<actor>1. LORD.</actor>
		<actor>2. LORD.</actor>
		<actor>3. LORD.</actor>
		<actor>4. LORD.</actor>
		<actor>Attendants</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="826.02" sdnumber="161.02">
	<dir>Lafew and Parolles stay behind, commenting of this wedding.</dir>
	<action type="action">
		<actor>LAF.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="827" number="162" form="prose">Do you hear, <foreign xml:lang="fr">monsieur</foreign>? A word with you.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="828" number="163" form="prose">Your pleasure, sir?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="829" number="164" form="prose">Your lord and master did well to make his recantation.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="830" number="165" form="prose">Recantation? My lord? My master?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="831" number="166" form="prose">Ay; is it not a language I speak?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="832" number="167" form="prose">A most harsh one, and not to be understood without bloody succeeding. My master?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="833" number="168" form="prose">Are you companion to the Count Roussillon?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="834" number="169" form="prose">To any count, to all counts: to what is man.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="835" number="170" form="prose">To what is count&#8217;s man. Count&#8217;s master is of another style.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="836" number="171" form="prose">You are too old, sir; let it satisfy you, you are too old.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="837" number="172" form="prose">I must tell thee, sirrah, I write man; to which title age cannot bring thee.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="838" number="173" form="prose">What I dare too well do, I dare not do.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="839" number="174" form="prose">I did think thee, for two ordinaries, to be a pretty wise fellow. Thou didst make tolerable vent of thy travel; it might pass: yet the scarfs and the bannerets about thee did manifoldly dissuade me from believing thee a vessel of too great a burden. I have now found thee. When I lose thee again, I care not; yet art thou good for nothing but taking up, and that thou&#8217;rt scarce worth.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="840" number="175" form="prose">Hadst thou not the privilege of antiquity upon thee&#8212;</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="841" number="176" form="prose">Do not plunge thyself too far in anger, lest thou hasten thy trial; which if&#8212;Lord have mercy on thee for a hen! So, my good window of lattice, fare thee well. Thy casement I need not open, for I look through thee. Give me thy hand.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="842" number="177" form="prose">My lord, you give me most egregious indignity.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="843" number="178" form="prose">Ay, with all my heart, and thou art worthy of it.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="844" number="179" form="prose">I have not, my lord, deserv&#8217;d it.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="845" number="180" form="prose">Yes, good faith, ev&#8217;ry dram of it, and I will not bate thee a scruple.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="846" number="181" form="prose">Well, I shall be wiser.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="847" number="182" form="prose">Ev&#8217;n as soon as thou canst, for thou hast to pull at a smack a&#8217; th&#8217; contrary. If ever thou be&#8217;st bound in thy scarf and beaten, thou shall find what it is to be proud of thy bondage. I have a desire to hold my acquaintance with thee, or rather my knowledge, that I may say in the default, &#8220;He is a man I know.&#8221;</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="848" number="183" form="prose">My lord, you do me most insupportable vexation.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="849" number="184" form="prose">I would it were hell-pains for thy sake, and my poor doing eternal; for doing I am past, as I will by thee, in what motion age will give me leave.</line>
</speech>

<stagedir sdglobalnumber="849.01" sdnumber="184.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>LAF.</actor>
	</action>
</stagedir>

<speech type="soliloquy">
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="850" number="185" form="prose">Well, thou hast a son shall take this disgrace off me, scurvy, old, filthy, scurvy lord! Well, I must be patient, there is no fettering of authority. I&#8217;ll beat him, by my life, if I can meet him with any convenience, and he were double and double a lord. I&#8217;ll have no more pity of his age than I would have of&#8212;I&#8217;ll beat him, and if I could but meet him again.</line>
</speech>

<stagedir sdglobalnumber="850.01" sdnumber="185.01">
	<dir>Enter Lafew.</dir>
	<action type="enter">
		<actor>LAF.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="851" number="186" form="prose">Sirrah, your lord and master&#8217;s married, there&#8217;s news for you. You have a new mistress.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="852" number="187" form="prose">I most unfeignedly beseech your lordship to make some reservation of your wrongs. He is my good lord; whom I serve above is my master.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="853" number="188" form="prose">Who? God?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="854" number="189" form="prose">Ay, sir.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="855" number="190" form="prose">The devil it is that&#8217;s thy master. Why dost thou garter up thy arms a&#8217; this fashion? Dost make hose of thy sleeves? Do other servants so? Thou wert best set thy lower part where thy nose stands. By mine honor, if I were but two hours younger, I&#8217;d beat thee. Methink&#8217;st thou art a general offense, and every man should beat thee. I think thou wast created for men to breathe themselves upon thee.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="856" number="191" form="prose">This is hard and undeserv&#8217;d measure, my lord.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="857" number="192" form="prose">Go to, sir, you were beaten in Italy for picking a kernel out of a pomegranate. You are a vagabond and no true traveler. You are more saucy with lords and honorable personages than the commission of your birth and virtue gives you heraldry. You are not worth another word, else I&#8217;d call you knave. I leave you.</line>
</speech>

<stagedir sdglobalnumber="857.01" sdnumber="192.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>LAF.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="857.02" sdnumber="192.02">
	<dir>Enter Bertram, Count Roussillon.</dir>
	<action type="enter">
		<actor>BER.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="858" number="193" form="prose">Good, very good, it is so then. Good, very good, let it be conceal&#8217;d awhile.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="859" number="194" form="verse">Undone, and forfeited to cares forever!</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="860" number="195" form="prose">What&#8217;s the matter, sweet heart?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="861" number="196" form="verse">Although before the solemn priest I have sworn,</line>
<line globalnumber="862" number="197" form="verse">I will not bed her.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="863" number="198" form="prose">What, what, sweet heart?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="864" number="199" form="verse">O my Parolles, they have married me!</line>
<line globalnumber="865" number="200" form="verse">I&#8217;ll to the Tuscan wars, and never bed her.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="866" number="201" form="verse">France is a dog-hole, and it no more merits</line>
<line globalnumber="867" number="202" form="verse">The tread of a man&#8217;s foot. To th&#8217; wars!</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="868" number="203" form="verse">There&#8217;s letters from my mother; what th&#8217; import is,</line>
<line globalnumber="869" number="204" form="verse">I know not yet.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="870" number="205" form="verse">Ay, that would be known. To th&#8217; wars, my boy, to th&#8217; wars!</line>
<line globalnumber="871" number="206" form="verse">He wears his honor in a box unseen,</line>
<line globalnumber="872" number="207" form="verse">That hugs his kicky-wicky here at home,</line>
<line globalnumber="873" number="208" form="verse">Spending his manly marrow in her arms,</line>
<line globalnumber="874" number="209" form="verse">Which should sustain the bound and high curvet</line>
<line globalnumber="875" number="210" form="verse">Of Mars&#8217;s fiery steed. To other regions!</line>
<line globalnumber="876" number="211" form="verse">France is a stable, we that dwell in&#8217;t jades,</line>
<line globalnumber="877" number="212" form="verse">Therefore to th&#8217; war!</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="878" number="213" form="verse">It shall be so. I&#8217;ll send her to my house,</line>
<line globalnumber="879" number="214" form="verse">Acquaint my mother with my hate to her,</line>
<line globalnumber="880" number="215" form="verse">And wherefore I am fled; write to the King</line>
<line globalnumber="881" number="216" form="verse">That which I durst not speak. His present gift</line>
<line globalnumber="882" number="217" form="verse">Shall furnish me to those Italian fields</line>
<line globalnumber="883" number="218" form="verse">Where noble fellows strike. Wars is no strife</line>
<line globalnumber="884" number="219" form="verse">To the dark house and the detested wife.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="885" number="220" form="verse">Will this <foreign xml:lang="it">capriccio</foreign> hold in thee, art sure?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="886" number="221" form="verse">Go with me to my chamber, and advise me.</line>
<line globalnumber="887" number="222" form="verse">I&#8217;ll send her straight away. Tomorrow,</line>
<line globalnumber="888" number="223" form="verse">I&#8217;ll to the wars, she to her single sorrow.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="889" number="224" form="verse">Why, these balls bound, there&#8217;s noise in it. &#8217;Tis hard!</line>
<line globalnumber="890" number="225" form="verse">A young man married is a man that&#8217;s marr&#8217;d;</line>
<line globalnumber="891" number="226" form="verse">Therefore away, and leave her bravely; go.</line>
<line globalnumber="892" number="227" form="verse">The King has done you wrong; but hush, &#8217;tis so.</line>
</speech>

<stagedir sdglobalnumber="892.01" sdnumber="227.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>BER.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="2" num="4">
<scenetitle>Scene 4</scenetitle>
<scenelocation>Another room in the King&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="HEL.">Helena</scenepersona>
	<scenepersona short="CLO.">Clown</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="892.02" sdnumber="0.01">
	<dir>Enter Helena and Clown.</dir>
	<action type="enter">
		<actor>HEL.</actor>
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="893" number="1" form="prose">My mother greets me kindly. Is she well?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="894" number="2" form="prose">She is not well, but yet she has her health. She&#8217;s very merry, but yet she is not well; but thanks be given, she&#8217;s very well, and wants nothing i&#8217; th&#8217; world; but yet she is not well.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="895" number="3" form="prose">If she be very well, what does she ail that she&#8217;s not very well?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="896" number="4" form="prose">Truly, she&#8217;s very well indeed, but for two things.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="897" number="5" form="prose">What two things?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="898" number="6" form="prose">One, that she&#8217;s not in heaven, whither God send her quickly! The other, that she&#8217;s in earth, from whence God send her quickly!</line>
</speech>

<stagedir sdglobalnumber="898.01" sdnumber="6.01">
	<dir>Enter Parolles.</dir>
	<action type="enter">
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="899" number="7" form="prose">Bless you, my fortunate lady!</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="900" number="8" form="prose">I hope, sir, I have your good will to have mine own good fortunes.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="901" number="9" form="prose">You had my prayers to lead them on, and to keep them on, have them still. O, my knave, how does my old lady?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="902" number="10" form="prose">So that you had her wrinkles and I her money, I would she did as you say.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="903" number="11" form="prose">Why, I say nothing.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="904" number="12" form="prose">Marry, you are the wiser man; for many a man&#8217;s tongue shakes out his master&#8217;s undoing. To say nothing, to do nothing, to know nothing, and to have nothing, is to be a great part of your title, which is within a very little of nothing.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="905" number="13" form="prose">Away, th&#8217; art a knave.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="906" number="14" form="prose">You should have said, sir, &#8220;Before a knave th&#8217; art a knave,&#8221; that&#8217;s &#8220;Before me th&#8217; art a knave.&#8221; This had been truth, sir.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="907" number="15" form="prose">Go to, thou art a witty fool, I have found thee.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="908" number="16" form="prose">Did you find me in yourself, sir,</line>
<stagedir sdglobalnumber="908.01" sdnumber="16.01">
	<dir>Parolles nods.</dir>
	<action type="action">
		<actor>PAR.</actor>
	</action>
</stagedir>
<line globalnumber="909" number="17" form="prose">or were you taught to find me?</line>
<stagedir sdglobalnumber="909.01" sdnumber="17.01">
	<dir>Parolles shakes his head.</dir>
	<action type="action">
		<actor>PAR.</actor>
	</action>
</stagedir>
<line globalnumber="910" number="18" form="prose">The search, sir, was profitable, and much fool may you find in you, even to the world&#8217;s pleasure and the increase of laughter.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="911" number="19" form="verse">A good knave, i&#8217; faith, and well fed.</line>
<line globalnumber="912" number="20" form="verse">Madam, my lord will go away tonight,</line>
<line globalnumber="913" number="21" form="verse">A very serious business calls on him.</line>
<line globalnumber="914" number="22" form="verse">The great prerogative and rite of love,</line>
<line globalnumber="915" number="23" form="verse">Which, as your due, time claims, he does acknowledge,</line>
<line globalnumber="916" number="24" form="verse">But puts it off to a compell&#8217;d restraint;</line>
<line globalnumber="917" number="25" form="verse">Whose want, and whose delay, is strew&#8217;d with sweets,</line>
<line globalnumber="918" number="26" form="verse">Which they distill now in the curbed time,</line>
<line globalnumber="919" number="27" form="verse">To make the coming hour o&#8217;erflow with joy,</line>
<line globalnumber="920" number="28" form="verse" offset="0">And pleasure drown the brim.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="921" number="28" form="verse" offset="6">What&#8217;s his will else?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="922" number="29" form="verse">That you will take your instant leave a&#8217; th&#8217; King,</line>
<line globalnumber="923" number="30" form="verse">And make this haste as your own good proceeding,</line>
<line globalnumber="924" number="31" form="verse">Strength&#8217;ned with what apology you think</line>
<line globalnumber="925" number="32" form="verse" offset="0">May make it probable need.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="926" number="32" form="verse" offset="5">What more commands he?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="927" number="33" form="verse">That having this obtain&#8217;d, you presently</line>
<line globalnumber="928" number="34" form="verse">Attend his further pleasure.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="929" number="35" form="verse">In every thing I wait upon his will.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="930" number="36" form="verse" offset="0">I shall report it so.</line>
</speech>

<stagedir sdglobalnumber="930.01" sdnumber="36.01">
	<dir>Exit Parolles.</dir>
	<action type="exit">
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="931" number="36" form="verse" offset="4">I pray you. Come, sirrah.</line>
</speech>

<stagedir sdglobalnumber="931.01" sdnumber="36.02">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>HEL.</actor>
		<actor>CLO.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="2" num="5">
<scenetitle>Scene 5</scenetitle>
<scenelocation>Another room in the King&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="LAF.">Lafew</scenepersona>
	<scenepersona short="BER.">Bertram</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
	<scenepersona short="HEL.">Helena</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="fr">French</language>
    <language short="it">Italian</language>
</scenelanguage>


<stagedir sdglobalnumber="931.02" sdnumber="0.01">
	<dir>Enter Lafew and Bertram.</dir>
	<action type="enter">
		<actor>LAF.</actor>
		<actor>BER.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="932" number="1" form="prose">But I hope your lordship thinks not him a soldier.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="933" number="2" form="prose">Yes, my lord, and of very valiant approof.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="934" number="3" form="prose">You have it from his own deliverance.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="935" number="4" form="prose">And by other warranted testimony.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="936" number="5" form="prose">Then my dial goes not true. I took this lark for a bunting.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="937" number="6" form="prose">I do assure you, my lord, he is very great in knowledge, and accordingly valiant.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="938" number="7" form="prose">I have then sinn&#8217;d against his experience, and transgress&#8217;d against his valor, and my state that way is dangerous, since I cannot yet find in my heart to repent. Here he comes. I pray you make us friends, I will pursue the amity.</line>
</speech>

<stagedir sdglobalnumber="938.01" sdnumber="7.01">
	<dir>Enter Parolles.</dir>
	<action type="enter">
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Parolles">PAR.</speaker>

<stagedir sdglobalnumber="938.02" sdnumber="7.02">
	<dir>To Bertram.</dir>
	<action type="speak">
		<actor>PAR.</actor>
		<recipient>BER.</recipient>
	</action>
</stagedir>
<line globalnumber="939" number="8" form="prose">These things shall be done, sir.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="940" number="9" form="prose">Pray you, sir, who&#8217;s his tailor?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="941" number="10" form="prose">Sir!</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="942" number="11" form="prose">O, I know him well, I, sir, he, sir, &#8217;s a good workman, a very good tailor.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>

<stagedir sdglobalnumber="942.01" sdnumber="11.01">
	<dir>Aside to Parolles.</dir>
	<action type="aside">
		<actor>BER.</actor>
		<recipient>PAR.</recipient>
	</action>
</stagedir>
<line globalnumber="943" number="12" form="prose">Is she gone to the King?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="944" number="13" form="prose">She is.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="945" number="14" form="prose">Will she away tonight?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="946" number="15" form="prose">As you&#8217;ll have her.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="947" number="16" form="verse">I have writ my letters, casketed my treasure,</line>
<line globalnumber="948" number="17" form="verse">Given order for our horses, and tonight,</line>
<line globalnumber="949" number="18" form="verse">When I should take possession of the bride,</line>
<line globalnumber="950" number="19" form="verse">End ere I do begin.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="951" number="20" form="prose">A good traveler is something at the latter end of a dinner, but one that lies three thirds, and uses a known truth to pass a thousand nothings with, should be once heard and thrice beaten. God save you, captain.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="952" number="21" form="prose">Is there any unkindness between my lord and you, <foreign xml:lang="fr">monsieur</foreign>?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="953" number="22" form="prose">I know not how I have deserv&#8217;d to run into my lord&#8217;s displeasure.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="954" number="23" form="prose">You have made shift to run into&#8217;t, boots and spurs and all, like him that leapt into the custard; and out of it you&#8217;ll run again, rather than suffer question for your residence.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="955" number="24" form="prose">It may be you have mistaken him, my lord.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="956" number="25" form="prose">And shall do so ever, though I took him at &#8217;s prayers. Fare you well, my lord, and believe this of me: there can be no kernel in this light nut; the soul of this man is his clothes. Trust him not in matter of heavy consequence; I have kept of them tame, and know their natures. Farewell, <foreign xml:lang="fr">monsieur</foreign>, I have spoken better of you than you have or will to deserve at my hand, but we must do good against evil.</line>
</speech>

<stagedir sdglobalnumber="956.01" sdnumber="25.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>LAF.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="957" number="26" form="prose">An idle lord, I swear.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="958" number="27" form="prose">I think so.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="959" number="28" form="prose">Why, do you not know him?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="960" number="29" form="verse">Yes, I do know him well, and common speech</line>
<line globalnumber="961" number="30" form="verse">Gives him a worthy pass. Here comes my clog.</line>
</speech>

<stagedir sdglobalnumber="961.01" sdnumber="30.01">
	<dir>Enter Helena.</dir>
	<action type="enter">
		<actor>HEL.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="962" number="31" form="verse">I have, sir, as I was commanded from you,</line>
<line globalnumber="963" number="32" form="verse">Spoke with the King, and have procur&#8217;d his leave</line>
<line globalnumber="964" number="33" form="verse">For present parting; only he desires</line>
<line globalnumber="965" number="34" form="verse" offset="0">Some private speech with you.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="966" number="34" form="verse" offset="6">I shall obey his will.</line>
<line globalnumber="967" number="35" form="verse">You must not marvel, Helen, at my course,</line>
<line globalnumber="968" number="36" form="verse">Which holds not color with the time, nor does</line>
<line globalnumber="969" number="37" form="verse">The ministration and required office</line>
<line globalnumber="970" number="38" form="verse">On my particular. Prepar&#8217;d I was not</line>
<line globalnumber="971" number="39" form="verse">For such a business; therefore am I found</line>
<line globalnumber="972" number="40" form="verse">So much unsettled. This drives me to entreat you</line>
<line globalnumber="973" number="41" form="verse">That presently you take your way for home,</line>
<line globalnumber="974" number="42" form="verse">And rather muse than ask why I entreat you,</line>
<line globalnumber="975" number="43" form="verse">For my respects are better than they seem,</line>
<line globalnumber="976" number="44" form="verse">And my appointments have in them a need</line>
<line globalnumber="977" number="45" form="verse">Greater than shows itself at the first view</line>
<line globalnumber="978" number="46" form="verse">To you that know them not. This to my mother.</line>
<stagedir sdglobalnumber="978.01" sdnumber="46.01">
	<dir>Giving a letter.</dir>
	<action type="action">
		<actor>BER.</actor>
		<recipient>HEL.</recipient>
	</action>
</stagedir>
<line globalnumber="979" number="47" form="verse">&#8217;Twill be two days ere I shall see you, so</line>
<line globalnumber="980" number="48" form="verse" offset="0">I leave you to your wisdom.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="981" number="48" form="verse" offset="5">Sir, I can nothing say,</line>
<line globalnumber="982" number="49" form="verse">But that I am your most obedient servant.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="983" number="50" form="verse" offset="0">Come, come, no more of that.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="984" number="50" form="verse" offset="6">And ever shall</line>
<line globalnumber="985" number="51" form="verse">With true observance seek to eke out that</line>
<line globalnumber="986" number="52" form="verse">Wherein toward me my homely stars have fail&#8217;d</line>
<line globalnumber="987" number="53" form="verse" offset="0">To equal my great fortune.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="988" number="53" form="verse" offset="5">Let that go.</line>
<line globalnumber="989" number="54" form="verse">My haste is very great. Farewell; hie home.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="990" number="55" form="verse" offset="0">Pray, sir, your pardon.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="991" number="55" form="verse" offset="4">Well, what would you say?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="992" number="56" form="verse">I am not worthy of the wealth I owe,</line>
<line globalnumber="993" number="57" form="verse">Nor dare I say &#8217;tis mine; and yet it is;</line>
<line globalnumber="994" number="58" form="verse">But like a timorous thief, most fain would steal</line>
<line globalnumber="995" number="59" form="verse" offset="0">What law does vouch mine own.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="996" number="59" form="verse" offset="7">What would you have?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="997" number="60" form="verse">Something, and scarce so much; nothing indeed.</line>
<line globalnumber="998" number="61" form="verse">I would not tell you what I would, my lord.</line>
<line globalnumber="999" number="62" form="verse">Faith, yes:</line>
<line globalnumber="1000" number="63" form="verse">Strangers and foes do sunder, and not kiss.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1001" number="64" form="verse">I pray you stay not, but in haste to horse.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1002" number="65" form="verse">I shall not break your bidding, good my lord.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1003" number="66" form="verse">Where are my other men, <foreign xml:lang="fr">monsieur</foreign>?&#8212;Farewell.</line>
<stagedir sdglobalnumber="1003.01" sdnumber="66.01">
	<dir>Exit Helena.</dir>
	<action type="exit">
		<actor>HEL.</actor>
	</action>
</stagedir>
<line globalnumber="1004" number="67" form="verse">Go thou toward home, where I will never come</line>
<line globalnumber="1005" number="68" form="verse">Whilst I can shake my sword or hear the drum.</line>
<line globalnumber="1006" number="69" form="verse">Away, and for our flight.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1007" number="70" form="verse">Bravely, <foreign xml:lang="it">coraggio</foreign>!</line>
</speech>

<stagedir sdglobalnumber="1007.01" sdnumber="70.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>BER.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

</scene>

</act>

<act num="3">
<acttitle>Act 3</acttitle>

<scene actnum="3" num="1">
<scenetitle>Scene 1</scenetitle>
<scenelocation>Florence. The Duke&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="DUKE.">Duke of Florence</scenepersona>
	<scenepersona short="BOTH LORDS.">two French Lords</scenepersona>
	<scenepersona short="1. SOLD. AS INTERPRETER.">First Soldier as Interpreter</scenepersona>
<scenepersona short="2. SOLD.">Second Soldier</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1007.02" sdnumber="0.01">
	<dir>Flourish. Enter the Duke of Florence, the two French Lords, with a troop of soldiers.</dir>
	<action type="enter">
		<actor>DUKE.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Duke of Florence">DUKE.</speaker>
<line globalnumber="1008" number="1" form="verse">So that from point to point now have you heard</line>
<line globalnumber="1009" number="2" form="verse">The fundamental reasons of this war,</line>
<line globalnumber="1010" number="3" form="verse">Whose great decision hath much blood let forth</line>
<line globalnumber="1011" number="4" form="verse" offset="0">And more thirsts after.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1012" number="4" form="verse" offset="4">Holy seems the quarrel</line>
<line globalnumber="1013" number="5" form="verse">Upon your Grace&#8217;s part; black and fearful</line>
<line globalnumber="1014" number="6" form="verse">On the opposer.</line>
</speech>

<speech>
<speaker long="Duke of Florence">DUKE.</speaker>
<line globalnumber="1015" number="7" form="verse">Therefore we marvel much our cousin France</line>
<line globalnumber="1016" number="8" form="verse">Would in so just a business shut his bosom</line>
<line globalnumber="1017" number="9" form="verse" offset="0">Against our borrowing prayers.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1018" number="9" form="verse" offset="6">Good my lord,</line>
<line globalnumber="1019" number="10" form="verse">The reasons of our state I cannot yield</line>
<line globalnumber="1020" number="11" form="verse">But like a common and an outward man</line>
<line globalnumber="1021" number="12" form="verse">That the great figure of a council frames</line>
<line globalnumber="1022" number="13" form="verse">By self-unable motion, therefore dare not</line>
<line globalnumber="1023" number="14" form="verse">Say what I think of it, since I have found</line>
<line globalnumber="1024" number="15" form="verse">Myself in my incertain grounds to fail</line>
<line globalnumber="1025" number="16" form="verse" offset="0">As often as I guess&#8217;d.</line>
</speech>

<speech>
<speaker long="Duke of Florence">DUKE.</speaker>
<line globalnumber="1026" number="16" form="verse" offset="4">Be it his pleasure.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1027" number="17" form="verse">But I am sure the younger of our nature,</line>
<line globalnumber="1028" number="18" form="verse">That surfeit on their ease, will day by day</line>
<line globalnumber="1029" number="19" form="verse" offset="0">Come here for physic.</line>
</speech>

<speech>
<speaker long="Duke of Florence">DUKE.</speaker>
<line globalnumber="1030" number="19" form="verse" offset="4">Welcome shall they be;</line>
<line globalnumber="1031" number="20" form="verse">And all the honors that can fly from us</line>
<line globalnumber="1032" number="21" form="verse">Shall on them settle.&#8212;You know your places well;</line>
<line globalnumber="1033" number="22" form="verse">When better fall, for your avails they fell.</line>
<line globalnumber="1034" number="23" form="verse">Tomorrow to th&#8217; field.</line>
</speech>

<stagedir sdglobalnumber="1034.01" sdnumber="23.01">
	<dir>Flourish. Exeunt.</dir>
	<action type="exit">
		<actor>DUKE.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="3" num="2">
<scenetitle>Scene 2</scenetitle>
<scenelocation>Rossillon. The Count&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="COUNT.">Countess</scenepersona>
	<scenepersona short="CLO.">Clown</scenepersona>
	<scenepersona short="HEL.">Helen</scenepersona>
	<scenepersona short="BOTH LORDS.">two French Lords</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1034.02" sdnumber="0.01">
	<dir>Enter Countess and Clown.</dir>
	<action type="enter">
		<actor>COUNT.</actor>
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1035" number="1" form="prose">It hath happen&#8217;d all as I would have had it, save that he comes not along with her.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1036" number="2" form="prose">By my troth, I take my young lord to be a very melancholy man.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1037" number="3" form="prose">By what observance, I pray you?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1038" number="4" form="prose">Why, he will look upon his boot and sing, mend the ruff and sing, ask questions and sing, pick his teeth and sing. I know a man that had this trick of melancholy sold a goodly manor for a song.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1039" number="5" form="prose">Let me see what he writes, and when he means to come.</line>
</speech>

<stagedir sdglobalnumber="1039.01" sdnumber="5.01">
	<dir>Opening a letter.</dir>
	<action type="action">
		<actor>COUNT.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1040" number="6" form="prose">I have no mind to Isbel since I was at court. Our old ling and our Isbels a&#8217; th&#8217; country are nothing like your old ling and your Isbels a&#8217; th&#8217; court. The brains of my Cupid&#8217;s knock&#8217;d out, and I begin to love, as an old man loves money, with no stomach.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1041" number="7" form="prose">What have we here?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1042" number="8" form="prose">E&#8217;en that you have there.</line>
</speech>

<stagedir sdglobalnumber="1042.01" sdnumber="8.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech type="soliloquy">
<speaker long="Countess of Roussillon">COUNT.</speaker>
<stagedir sdglobalnumber="1042.02" sdnumber="8.02">
	<dir>Reads a letter.</dir>
	<action type="read">
		<actor>COUNT.</actor>
	</action>
</stagedir>
<line globalnumber="1043" number="9" form="prose"><recite>&#8220;I have sent you a daughter-in-law; she hath recover&#8217;d the King, and undone me. I have wedded her, not bedded her, and sworn to make the &#8220;not&#8221; eternal. You shall hear I am run away; know it before the report come. If there be breadth enough in the world, I will hold a long distance. My duty to you.</recite></line>
<line globalnumber="1044" number="10" form="prose"><recite>Your unfortunate son, Bertram.&#8221;</recite></line><lb />
<line globalnumber="1045" number="11" form="verse">This is not well, rash and unbridled boy,</line>
<line globalnumber="1046" number="12" form="verse">To fly the favors of so good a king,</line>
<line globalnumber="1047" number="13" form="verse">To pluck his indignation on thy head</line>
<line globalnumber="1048" number="14" form="verse">By the misprising of a maid too virtuous</line>
<line globalnumber="1049" number="15" form="verse">For the contempt of empire.</line>
</speech>

<stagedir sdglobalnumber="1049.01" sdnumber="15.01">
	<dir>Enter Clown.</dir>
	<action type="enter">
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1050" number="16" form="prose">O madam, yonder is heavy news within between two soldiers and my young lady!</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1051" number="17" form="prose">What is the matter?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1052" number="18" form="prose">Nay, there is some comfort in the news, some comfort. Your son will not be kill&#8217;d so soon as I thought he would.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1053" number="19" form="prose">Why should he be kill&#8217;d?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1054" number="20" form="prose">So say I, madam, if he run away, as I hear he does. The danger is in standing to&#8217;t; that&#8217;s the loss of men, though it be the getting of children. Here they come will tell you more; for my part, I only hear your son was run away.</line>
</speech>

<stagedir sdglobalnumber="1054.01" sdnumber="20.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>CLO.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="1054.02" sdnumber="20.02">
	<dir>Enter Helen and two French Lords.</dir>
	<action type="enter">
		<actor>HEL.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1055" number="21" form="prose">&#8217;Save you, good madam.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1056" number="22" form="prose">Madam, my lord is gone, forever gone.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1057" number="23" form="prose">Do not say so.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1058" number="24" form="verse">Think upon patience. Pray you, gentlemen,</line>
<line globalnumber="1059" number="25" form="verse">I have felt so many quirks of joy and grief</line>
<line globalnumber="1060" number="26" form="verse">That the first face of neither on the start</line>
<line globalnumber="1061" number="27" form="verse">Can woman me unto&#8217;t. Where is my son, I pray you?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1062" number="28" form="verse">Madam, he&#8217;s gone to serve the Duke of Florence.</line>
<line globalnumber="1063" number="29" form="verse">We met him thitherward, for thence we came;</line>
<line globalnumber="1064" number="30" form="verse">And after some dispatch in hand at court,</line>
<line globalnumber="1065" number="31" form="verse">Thither we bend again.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1066" number="32" form="verse">Look on his letter, madam, here&#8217;s my passport.</line>
<stagedir sdglobalnumber="1066.01" sdnumber="32.01">
	<dir>Reads.</dir>
	<action type="read">
		<actor>HEL.</actor>
	</action>
</stagedir>
<line globalnumber="1067" number="33" form="prose"><recite>&#8220;When thou canst get the ring upon my finger, which never shall come off, and show me a child begotten of thy body that I am father to, then call me husband; but in such a &#8216;then&#8217; I write a &#8216;never.&#8217;&#8221; </recite></line>
<line globalnumber="1068" number="34" form="verse">This is a dreadful sentence.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1069" number="35" form="verse" offset="0">Brought you this letter, gentlemen?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1070" number="35" form="verse" offset="7">Ay, madam,</line>
<line globalnumber="1071" number="36" form="verse">And for the contents&#8217; sake are sorry for our pains.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1072" number="37" form="verse">I prithee, lady, have a better cheer;</line>
<line globalnumber="1073" number="38" form="verse">If thou engrossest all the griefs are thine,</line>
<line globalnumber="1074" number="39" form="verse">Thou robb&#8217;st me of a moi&#8217;ty. He was my son,</line>
<line globalnumber="1075" number="40" form="verse">But I do wash his name out of my blood,</line>
<line globalnumber="1076" number="41" form="verse">And thou art all my child. Towards Florence is he?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1077" number="42" form="verse" offset="0">Ay, madam.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1078" number="42" form="verse" offset="3">And to be a soldier?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1079" number="43" form="verse">Such is his noble purpose, and believe&#8217;t,</line>
<line globalnumber="1080" number="44" form="verse">The Duke will lay upon him all the honor</line>
<line globalnumber="1081" number="45" form="verse" offset="0">That good convenience claims.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1082" number="45" form="verse" offset="6">Return you thither?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1083" number="46" form="verse">Ay, madam, with the swiftest wing of speed.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<stagedir sdglobalnumber="1083.01" sdnumber="46.01">
	<dir>Reads.</dir>
	<action type="read">
		<actor>HEL.</actor>
	</action>
</stagedir>
<line globalnumber="1084" number="47" form="prose"><recite>&#8220;Till I have no wife, I have nothing in France.&#8221;</recite></line><lb />
<line globalnumber="1085" number="48" form="verse" offset="0">&#8217;Tis bitter.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1086" number="48" form="verse" offset="2">Find you that there?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1087" number="48" form="verse" offset="7">Ay, madam.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1088" number="49" form="verse">&#8217;Tis but the boldness of his hand haply,</line>
<line globalnumber="1089" number="50" form="verse">Which his heart was not consenting to.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1090" number="51" form="verse">Nothing in France, until he have no wife!</line>
<line globalnumber="1091" number="52" form="verse">There&#8217;s nothing here that is too good for him</line>
<line globalnumber="1092" number="53" form="verse">But only she, and she deserves a lord</line>
<line globalnumber="1093" number="54" form="verse">That twenty such rude boys might tend upon,</line>
<line globalnumber="1094" number="55" form="verse">And call her hourly mistress. Who was with him?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1095" number="56" form="verse">A servant only, and a gentleman</line>
<line globalnumber="1096" number="57" form="verse" offset="0">Which I have sometime known.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1097" number="57" form="verse" offset="6">Parolles, was it not?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1098" number="58" form="verse">Ay, my good lady, he.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1099" number="59" form="verse">A very tainted fellow, and full of wickedness.</line>
<line globalnumber="1100" number="60" form="verse">My son corrupts a well-derived nature</line>
<line globalnumber="1101" number="61" form="verse" offset="0">With his inducement.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1102" number="61" form="verse" offset="4">Indeed, good lady,</line>
<line globalnumber="1103" number="62" form="verse">The fellow has a deal of that too much,</line>
<line globalnumber="1104" number="63" form="verse">Which holds him much to have.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1105" number="64" form="verse">Y&#8217; are welcome, gentlemen.</line>
<line globalnumber="1106" number="65" form="verse">I will entreat you, when you see my son,</line>
<line globalnumber="1107" number="66" form="verse">To tell him that his sword can never win</line>
<line globalnumber="1108" number="67" form="verse">The honor that he loses. More I&#8217;ll entreat you</line>
<line globalnumber="1109" number="68" form="verse" offset="0">Written to bear along.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1110" number="68" form="verse" offset="4">We serve you, madam,</line>
<line globalnumber="1111" number="69" form="verse">In that and all your worthiest affairs.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1112" number="70" form="verse">Not so, but as we change our courtesies.</line>
<line globalnumber="1113" number="71" form="verse">Will you draw near?</line>
</speech>

<stagedir sdglobalnumber="1113.01" sdnumber="71.01">
	<dir>Exit with Lords.</dir>
	<action type="exit">
		<actor>COUNT.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>

<speech type="soliloquy">
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1114" number="72" form="verse">&#8220;Till I have no wife, I have nothing in France.&#8221;</line>
<line globalnumber="1115" number="73" form="verse">Nothing in France, until he has no wife!</line>
<line globalnumber="1116" number="74" form="verse">Thou shalt have none, Roussillon, none in France;</line>
<line globalnumber="1117" number="75" form="verse">Then hast thou all again. Poor lord, is&#8217;t I</line>
<line globalnumber="1118" number="76" form="verse">That chase thee from thy country, and expose</line>
<line globalnumber="1119" number="77" form="verse">Those tender limbs of thine to the event</line>
<line globalnumber="1120" number="78" form="verse">Of the none-sparing war? And is it I</line>
<line globalnumber="1121" number="79" form="verse">That drive thee from the sportive court, where thou</line>
<line globalnumber="1122" number="80" form="verse">Wast shot at with fair eyes, to be the mark</line>
<line globalnumber="1123" number="81" form="verse">Of smoky muskets? O you leaden messengers,</line>
<line globalnumber="1124" number="82" form="verse">That ride upon the violent speed of fire,</line>
<line globalnumber="1125" number="83" form="verse">Fly with false aim, move the still-peering air</line>
<line globalnumber="1126" number="84" form="verse">That sings with piercing, do not touch my lord.</line>
<line globalnumber="1127" number="85" form="verse">Whoever shoots at him, I set him there;</line>
<line globalnumber="1128" number="86" form="verse">Whoever charges on his forward breast,</line>
<line globalnumber="1129" number="87" form="verse">I am the caitiff that do hold him to&#8217;t;</line>
<line globalnumber="1130" number="88" form="verse">And though I kill him not, I am the cause</line>
<line globalnumber="1131" number="89" form="verse">His death was so effected. Better &#8217;twere</line>
<line globalnumber="1132" number="90" form="verse">I met the ravin lion when he roar&#8217;d</line>
<line globalnumber="1133" number="91" form="verse">With sharp constraint of hunger; better &#8217;twere</line>
<line globalnumber="1134" number="92" form="verse">That all the miseries which nature owes</line>
<line globalnumber="1135" number="93" form="verse">Were mine at once. No, come thou home, Roussillon,</line>
<line globalnumber="1136" number="94" form="verse">Whence honor but of danger wins a scar,</line>
<line globalnumber="1137" number="95" form="verse">As oft it loses all. I will be gone.</line>
<line globalnumber="1138" number="96" form="verse">My being here it is that holds thee hence.</line>
<line globalnumber="1139" number="97" form="verse">Shall I stay here to do&#8217;t? No, no, although</line>
<line globalnumber="1140" number="98" form="verse">The air of paradise did fan the house,</line>
<line globalnumber="1141" number="99" form="verse">And angels offic&#8217;d all. I will be gone,</line>
<line globalnumber="1142" number="100" form="verse">That pitiful rumor may report my flight</line>
<line globalnumber="1143" number="101" form="verse">To consolate thine ear. Come night, end day!</line>
<line globalnumber="1144" number="102" form="verse">For with the dark, poor thief, I&#8217;ll steal away.</line>
</speech>

<stagedir sdglobalnumber="1144.01" sdnumber="102.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>HEL.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="3" num="3">
<scenetitle>Scene 3</scenetitle>
<scenelocation>Florence. Before the Duke&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="DUKE.">Duke of Florence</scenepersona>
	<scenepersona short="BER.">Bertram Count of Roussillon</scenepersona>
	<scenepersona short="1. SOLD. AS INTERPRETER.">First Soldier as Interpreter</scenepersona>
	<scenepersona short="2. SOLD.">Second Soldier</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1144.02" sdnumber="0.01">
	<dir>Flourish. Enter the Duke of Florence, Bertram Count of Roussillon, Drum and Trumpets, Soldiers, Parolles.</dir>
	<action type="enter">
		<actor>DUKE.</actor>
		<actor>BER.</actor>
		<actor>PAR.</actor>
		<actor>1. SOLD. AS INTERPRETER.</actor>
		<actor>2. SOLD.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Duke of Florence">DUKE.</speaker>
<line globalnumber="1145" number="1" form="verse">The general of our horse thou art, and we,</line>
<line globalnumber="1146" number="2" form="verse">Great in our hope, lay our best love and credence</line>
<line globalnumber="1147" number="3" form="verse" offset="0">Upon thy promising fortune.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1148" number="3" form="verse" offset="6">Sir, it is</line>
<line globalnumber="1149" number="4" form="verse">A charge too heavy for my strength, but yet</line>
<line globalnumber="1150" number="5" form="verse">We&#8217;ll strive to bear it for your worthy sake</line>
<line globalnumber="1151" number="6" form="verse" offset="0">To th&#8217; extreme edge of hazard.</line>
</speech>

<speech>
<speaker long="Duke of Florence">DUKE.</speaker>
<line globalnumber="1152" number="6" form="verse" offset="6">Then go thou forth,</line>
<line globalnumber="1153" number="7" form="verse">And Fortune play upon thy prosperous helm</line>
<line globalnumber="1154" number="8" form="verse" offset="0">As thy auspicious mistress!</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1155" number="8" form="verse" offset="5">This very day,</line>
<line globalnumber="1156" number="9" form="verse">Great Mars, I put myself into thy file;</line>
<line globalnumber="1157" number="10" form="verse">Make me but like my thoughts, and I shall prove</line>
<line globalnumber="1158" number="11" form="verse">A lover of thy drum, hater of love.</line>
</speech>

<stagedir sdglobalnumber="1158.01" sdnumber="11.01">
	<dir>Exeunt omnes.</dir>
	<action type="exit">
		<actor>DUKE.</actor>
		<actor>BER.</actor>
		<actor>PAR.</actor>
		<actor>1. SOLD. AS INTERPRETER.</actor>
		<actor>2. SOLD.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="3" num="4">
<scenetitle>Scene 4</scenetitle>
<scenelocation>Roussillon. The Count&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="COUNT.">Countess</scenepersona>
	<scenepersona short="STEW.">Steward Rinaldo</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1158.02" sdnumber="0.01">
	<dir>Enter Countess and Steward Rinaldo.</dir>
	<action type="enter">
		<actor>COUNT.</actor>
		<actor>STEW.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1159" number="1" form="verse">Alas! And would you take the letter of her?</line>
<line globalnumber="1160" number="2" form="verse">Might you not know she would do as she has done</line>
<line globalnumber="1161" number="3" form="verse">By sending me a letter? Read it again.</line>
</speech>

<speech>
<speaker long="Rinaldo">STEW.</speaker>
<line globalnumber="1162" number="4" form="verse">Reads letter.</line>
<line globalnumber="1163" number="5" form="verse"><recite>&#8220;I am Saint Jaques&#8217; pilgrim, thither gone.</recite></line>
<line globalnumber="1164" number="6" form="verse"><recite>Ambitious love hath so in me offended</recite></line>
<line globalnumber="1165" number="7" form="verse"><recite>That barefoot plod I the cold ground upon</recite></line>
<line globalnumber="1166" number="8" form="verse"><recite>With sainted vow my faults to have amended.</recite></line>
<line globalnumber="1167" number="9" form="verse"><recite>Write, write, that from the bloody course of war</recite></line>
<line globalnumber="1168" number="10" form="verse"><recite>My dearest master, your dear son, may hie.</recite></line>
<line globalnumber="1169" number="11" form="verse"><recite>Bless him at home in peace, whilst I from far</recite></line>
<line globalnumber="1170" number="12" form="verse"><recite>His name with zealous fervor sanctify.</recite></line>
<line globalnumber="1171" number="13" form="verse"><recite>His taken labors bid him me forgive;</recite></line>
<line globalnumber="1172" number="14" form="verse"><recite>I, his despiteful Juno, sent him forth</recite></line>
<line globalnumber="1173" number="15" form="verse"><recite>From courtly friends, with camping foes to live,</recite></line>
<line globalnumber="1174" number="16" form="verse"><recite>Where death and danger dogs the heels of worth.</recite></line>
<line globalnumber="1175" number="17" form="verse"><recite>He is too good and fair for death and me,</recite></line>
<line globalnumber="1176" number="18" form="verse"><recite>Whom I myself embrace to set him free.&#8221;</recite></line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1177" number="19" form="verse">Ah, what sharp stings are in her mildest words!</line>
<line globalnumber="1178" number="20" form="verse">Rinaldo, you did never lack advice so much</line>
<line globalnumber="1179" number="21" form="verse">As letting her pass so. Had I spoke with her,</line>
<line globalnumber="1180" number="22" form="verse">I could have well diverted her intents,</line>
<line globalnumber="1181" number="23" form="verse" offset="0">Which thus she hath prevented.</line>
</speech>

<speech>
<speaker long="Rinaldo">STEW.</speaker>
<line globalnumber="1182" number="23" form="verse" offset="6">Pardon me, madam,</line>
<line globalnumber="1183" number="24" form="verse">If I had given you this at overnight,</line>
<line globalnumber="1184" number="25" form="verse">She might have been o&#8217;erta&#8217;en; and yet she writes,</line>
<line globalnumber="1185" number="26" form="verse" offset="0">Pursuit would be but vain.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1186" number="26" form="verse" offset="5">What angel shall</line>
<line globalnumber="1187" number="27" form="verse">Bless this unworthy husband? He cannot thrive,</line>
<line globalnumber="1188" number="28" form="verse">Unless her prayers, whom heaven delights to hear</line>
<line globalnumber="1189" number="29" form="verse">And loves to grant, reprieve him from the wrath</line>
<line globalnumber="1190" number="30" form="verse">Of greatest justice. Write, write, Rinaldo,</line>
<line globalnumber="1191" number="31" form="verse">To this unworthy husband of his wife.</line>
<line globalnumber="1192" number="32" form="verse">Let every word weigh heavy of her worth,</line>
<line globalnumber="1193" number="33" form="verse">That he does weigh too light. My greatest grief,</line>
<line globalnumber="1194" number="34" form="verse">Though little he do feel it, set down sharply.</line>
<line globalnumber="1195" number="35" form="verse">Dispatch the most convenient messenger.</line>
<line globalnumber="1196" number="36" form="verse">When haply he shall hear that she is gone,</line>
<line globalnumber="1197" number="37" form="verse">He will return, and hope I may that she,</line>
<line globalnumber="1198" number="38" form="verse">Hearing so much, will speed her foot again,</line>
<line globalnumber="1199" number="39" form="verse">Led hither by pure love. Which of them both</line>
<line globalnumber="1200" number="40" form="verse">Is dearest to me, I have no skill in sense</line>
<line globalnumber="1201" number="41" form="verse">To make distinction. Provide this messenger.</line>
<line globalnumber="1202" number="42" form="verse">My heart is heavy, and mine age is weak;</line>
<line globalnumber="1203" number="43" form="verse">Grief would have tears, and sorrow bids me speak.</line>
</speech>

<stagedir sdglobalnumber="1203.01" sdnumber="43.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>COUNT.</actor>
		<actor>STEW.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="3" num="5">
<scenetitle>Scene 5</scenetitle>
<scenelocation>Without the walls of Florence.</scenelocation>

<scenepersonae>
	<scenepersona short="WID.">Old Widow of Florence</scenepersona>
	<scenepersona short="DIA.">Diana</scenepersona>
	<scenepersona short="VIOL.">Violenta</scenepersona>
	<scenepersona short="MAR.">Mariana</scenepersona>
	<scenepersona>Citizens</scenepersona>
	<scenepersona short="HEL.">Helen</scenepersona>
	<scenepersona short="BER.">Bertram Count Roussillon</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="fr">French</language>
</scenelanguage>


<stagedir sdglobalnumber="1203.02" sdnumber="0.01">
	<dir>A tucket afar off. Enter old Widow of Florence, her daughter, Diana, Violenta, and Mariana, with other Citizens.</dir>
	<action type="sound">
	</action>
	<action type="enter">
		<actor>WID.</actor>
		<actor>DIA.</actor>
		<actor>MAR.</actor>
		<actor>VIO.</actor>
		<actor>Citizens</actor>
	</action>
</stagedir>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1204" number="1" form="prose">Nay, come, for if they do approach the city, we shall lose all the sight.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1205" number="2" form="prose">They say the French count has done most honorable service.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1206" number="3" form="prose">It is reported that he has taken their great&#8217;st commander, and that with his own hand he slew the Duke&#8217;s brother. Tucket. We have lost our labor, they are gone a contrary way. Hark! You may know by their trumpets.</line>
</speech>

<speech>
<speaker long="Mariana">MAR.</speaker>
<line globalnumber="1207" number="4" form="prose">Come, let&#8217;s return again and suffice ourselves with the report of it. Well, Diana, take heed of this French earl. The honor of a maid is her name, and no legacy is so rich as honesty.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1208" number="5" form="prose">I have told my neighbor how you have been solicited by a gentleman his companion.</line>
</speech>

<speech>
<speaker long="Mariana">MAR.</speaker>
<line globalnumber="1209" number="6" form="prose">I know that knave, hang him! One Parolles, a filthy officer he is in those suggestions for the young earl. Beware of them, Diana; their promises, enticements, oaths, tokens, and all these engines of lust, are not the things they go under. Many a maid hath been seduc&#8217;d by them, and the misery is, example, that so terrible shows in the wrack of maidenhood, cannot for all that dissuade succession, but that they are lim&#8217;d with the twigs that threatens them. I hope I need not to advise you further, but I hope your own grace will keep you where you are, though there were no further danger known but the modesty which is so lost.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1210" number="7" form="verse">You shall not need to fear me.</line>
</speech>

<stagedir sdglobalnumber="1210.01" sdnumber="7.01">
	<dir>Enter Helen habited like a pilgrim.</dir>
	<action type="enter">
		<actor>HEL.</actor>
	</action>
</stagedir>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1211" number="8" form="prose">I hope so. Look here comes a pilgrim. I know she will lie at my house; thither they send one another. I&#8217;ll question her. God save you, pilgrim, whither are bound?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1212" number="9" form="verse">To Saint Jaques le Grand.</line>
<line globalnumber="1213" number="10" form="verse">Where do the palmers lodge, I do beseech you?</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1214" number="11" form="verse">At the Saint Francis here beside the port.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1215" number="12" form="verse">Is this the way?</line>
</speech>

<stagedir sdglobalnumber="1215.01" sdnumber="12.01">
	<dir>A march afar.</dir>
	<action type="sound">
	</action>
</stagedir>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1216" number="13" form="verse">Ay, marry, is&#8217;t. Hark you, they come this way.</line>
<line globalnumber="1217" number="14" form="verse">If you will tarry, holy pilgrim,</line>
<line globalnumber="1218" number="15" form="verse">But till the troops come by,</line>
<line globalnumber="1219" number="16" form="verse">I will conduct you where you shall be lodg&#8217;d,</line>
<line globalnumber="1220" number="17" form="verse">The rather for I think I know your hostess</line>
<line globalnumber="1221" number="18" form="verse" offset="0">As ample as myself.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1222" number="18" form="verse" offset="4">Is it yourself?</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1223" number="19" form="verse">If you shall please so, pilgrim.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1224" number="20" form="verse">I thank you, and will stay upon your leisure.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1225" number="21" form="verse" offset="0">You came I think from France?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1226" number="21" form="verse" offset="7">I did so.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1227" number="22" form="verse">Here you shall see a countryman of yours</line>
<line globalnumber="1228" number="23" form="verse" offset="0">That has done worthy service.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1229" number="23" form="verse" offset="6">His name, I pray you?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1230" number="24" form="verse">The Count Roussillon. Know you such a one?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1231" number="25" form="verse">But by the ear, that hears most nobly of him.</line>
<line globalnumber="1232" number="26" form="verse" offset="0">His face I know not.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1233" number="26" form="verse" offset="4">Whatsome&#8217;er he is,</line>
<line globalnumber="1234" number="27" form="verse">He&#8217;s bravely taken here. He stole from France,</line>
<line globalnumber="1235" number="28" form="verse">As &#8217;tis reported, for the King had married him</line>
<line globalnumber="1236" number="29" form="verse">Against his liking. Think you it is so?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1237" number="30" form="verse">Ay, surely, mere the truth, I know his lady.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1238" number="31" form="verse">There is a gentleman that serves the Count</line>
<line globalnumber="1239" number="32" form="verse" offset="0">Reports but coarsely of her.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1240" number="32" form="verse" offset="5">What&#8217;s his name?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1241" number="33" form="verse" offset="0"><foreign xml:lang="fr">Monsieur</foreign> Parolles.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1242" number="33" form="verse" offset="4">O, I believe with him.</line>
<line globalnumber="1243" number="34" form="verse">In argument of praise, or to the worth</line>
<line globalnumber="1244" number="35" form="verse">Of the great Count himself, she is too mean</line>
<line globalnumber="1245" number="36" form="verse">To have her name repeated. All her deserving</line>
<line globalnumber="1246" number="37" form="verse">Is a reserved honesty, and that</line>
<line globalnumber="1247" number="38" form="verse" offset="0">I have not heard examin&#8217;d.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1248" number="38" form="verse" offset="5">Alas, poor lady,</line>
<line globalnumber="1249" number="39" form="verse">&#8217;Tis a hard bondage to become the wife</line>
<line globalnumber="1250" number="40" form="verse">Of a detesting lord.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1251" number="41" form="verse">I warr&#8217;nt, good creature, wheresoe&#8217;er she is,</line>
<line globalnumber="1252" number="42" form="verse">Her heart weighs sadly. This young maid might do her</line>
<line globalnumber="1253" number="43" form="verse" offset="0">A shrewd turn, if she pleas&#8217;d.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1254" number="43" form="verse" offset="6">How do you mean?</line>
<line globalnumber="1255" number="44" form="verse">May be the amorous Count solicits her</line>
<line globalnumber="1256" number="45" form="verse" offset="0">In the unlawful purpose.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1257" number="45" form="verse" offset="5">He does indeed,</line>
<line globalnumber="1258" number="46" form="verse">And brokes with all that can in such a suit</line>
<line globalnumber="1259" number="47" form="verse">Corrupt the tender honor of a maid.</line>
<line globalnumber="1260" number="48" form="verse">But she is arm&#8217;d for him, and keeps her guard</line>
<line globalnumber="1261" number="49" form="verse" offset="0">In honestest defense.</line>
</speech>

<stagedir sdglobalnumber="1261.01" sdnumber="49.01">
	<dir>Drum and Colors. Enter (Bertram) Count Roussillon, Parolles, and the whole army.</dir>
	<action type="sound">
	</action>
	<action type="enter">
		<actor>BER.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Mariana">MAR.</speaker>
<line globalnumber="1262" number="49" form="verse" offset="4">The gods forbid else!</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1263" number="50" form="verse">So, now they come.</line>
<line globalnumber="1264" number="51" form="verse">That is Antonio, the Duke&#8217;s eldest son,</line>
<line globalnumber="1265" number="52" form="verse" offset="0">That, Escalus.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1266" number="52" form="verse" offset="3">Which is the Frenchman?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1267" number="52" form="verse" offset="8">He,</line>
<line globalnumber="1268" number="53" form="verse">That with the plume; &#8217;tis a most gallant fellow.</line>
<line globalnumber="1269" number="54" form="verse">I would he lov&#8217;d his wife. If he were honester</line>
<line globalnumber="1270" number="55" form="verse">He were much goodlier. Is&#8217;t not a handsome gentleman?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1271" number="56" form="verse">I like him well.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1272" number="57" form="verse">&#8217;Tis pity he is not honest. Yond&#8217;s that same knave</line>
<line globalnumber="1273" number="58" form="verse">That leads him to these places. Were I his lady,</line>
<line globalnumber="1274" number="59" form="verse" offset="0">I would poison that vile rascal.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1275" number="59" form="verse" offset="6">Which is he?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1276" number="60" form="prose">That jack-an-apes with scarfs. Why is he melancholy?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1277" number="61" form="prose">Perchance he&#8217;s hurt i&#8217; th&#8217; battle.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1278" number="62" form="prose">Lose our drum! Well.</line>
</speech>

<speech>
<speaker long="Mariana">MAR.</speaker>
<line globalnumber="1279" number="63" form="prose">He&#8217;s shrewdly vex&#8217;d at something. Look, he has spied us.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1280" number="64" form="prose">Marry, hang you!</line>
</speech>

<speech>
<speaker long="Mariana">MAR.</speaker>
<line globalnumber="1281" number="65" form="prose">And your courtesy, for a ring-carrier!</line>
</speech>

<stagedir sdglobalnumber="1281.01" sdnumber="65.01">
	<dir>Exeunt Bertram, Parolles, and army.</dir>
	<action type="exit">
		<actor>BER.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1282" number="66" form="verse">The troop is past. Come, pilgrim, I will bring you</line>
<line globalnumber="1283" number="67" form="verse">Where you shall host. Of enjoin&#8217;d penitents</line>
<line globalnumber="1284" number="68" form="verse">There&#8217;s four or five, to great Saint Jaques bound,</line>
<line globalnumber="1285" number="69" form="verse" offset="0">Already at my house.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1286" number="69" form="verse" offset="4">I humbly thank you.</line>
<line globalnumber="1287" number="70" form="verse">Please it this matron and this gentle maid</line>
<line globalnumber="1288" number="71" form="verse">To eat with us tonight, the charge and thanking</line>
<line globalnumber="1289" number="72" form="verse">Shall be for me, and to requite you further,</line>
<line globalnumber="1290" number="73" form="verse">I will bestow some precepts of this virgin</line>
<line globalnumber="1291" number="74" form="verse" offset="0">Worthy the note.</line>
</speech>

<speech>
<speaker long="Both Mariana and Widow">BOTH MAR. AND WID.</speaker>
<line globalnumber="1292" number="74" form="verse" offset="4">We&#8217;ll take your offer kindly.</line>
</speech>

<stagedir sdglobalnumber="1292.01" sdnumber="74.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>WID.</actor>
		<actor>DIA.</actor>
		<actor>MAR.</actor>
		<actor>VIO.</actor>
		<actor>Citizens</actor>
		<actor>HEL.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="3" num="6">
<scenetitle>Scene 6</scenetitle>
<scenelocation>Camp before Florence.</scenelocation>

<scenepersonae>
	<scenepersona short="BER.">Bertram Count Roussillon</scenepersona>
	<scenepersona short="BOTH LORDS.">two French Lords</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="la">Latin</language>
    <language short="fr">French</language>
</scenelanguage>


<stagedir sdglobalnumber="1292.02" sdnumber="0.01">
	<dir>Enter (Bertram) Count Roussillon and the two French Lords.</dir>
	<action type="enter">
		<actor>BER.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1293" number="1" form="prose">Nay, good my lord, put him to&#8217;t; let him have his way.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1294" number="2" form="prose">If your lordship find him not a hilding, hold me no more in your respect.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1295" number="3" form="prose">On my life, my lord, a bubble.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1296" number="4" form="prose">Do you think I am so far deceiv&#8217;d in him?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1297" number="5" form="prose">Believe it, my lord, in mine own direct knowledge, without any malice, but to speak of him as my kinsman, he&#8217;s a most notable coward, an infinite and endless liar, an hourly promise-breaker, the owner of no one good quality worthy your lordship&#8217;s entertainment.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1298" number="6" form="prose">It were fit you knew him, lest reposing too far in his virtue, which he hath not, he might at some great and trusty business in a main danger fail you.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1299" number="7" form="prose">I would I knew in what particular action to try him.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1300" number="8" form="prose">None better than to let him fetch off his drum, which you hear him so confidently undertake to do.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1301" number="9" form="prose">I, with a troop of Florentines, will suddenly surprise him; such I will have, whom I am sure he knows not from the enemy. We will bind and hoodwink him so, that he shall suppose no other but that he is carried into the leaguer of the adversaries, when we bring him to our own tents. Be but your lordship present at his examination, if he do not, for the promise of his life, and in the highest compulsion of base fear, offer to betray you, and deliver all the intelligence in his power against you, and that with the divine forfeit of his soul upon oath, never trust my judgment in any thing.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1302" number="10" form="prose">O, for the love of laughter, let him fetch his drum; he says he has a stratagem for&#8217;t. When your lordship sees the bottom of his success in&#8217;t, and to what metal this counterfeit lump of ore will be melted, if you give him not John Drum&#8217;s entertainment, your inclining cannot be remov&#8217;d. Here he comes.</line>
</speech>

<stagedir sdglobalnumber="1302.01" sdnumber="10.01">
	<dir>Enter Parolles.</dir>
	<action type="enter">
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1303" number="11" form="prose">O, for the love of laughter, hinder not the honor of his design. Let him fetch off his drum in any hand.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1304" number="12" form="prose">How now, <foreign xml:lang="fr">monsieur</foreign>? This drum sticks sorely in your disposition.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1305" number="13" form="prose">A pox on&#8217;t, let it go, &#8217;tis but a drum.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1306" number="14" form="prose">But a drum! Is&#8217;t but a drum? A drum so lost! There was excellent command&#8212;to charge in with our horse upon our own wings, and to rend our own soldiers!</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1307" number="15" form="prose">That was not to be blam&#8217;d in the command of the service; it was a disaster of war that Caesar himself could not have prevented, if he had been there to command.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1308" number="16" form="prose">Well, we cannot greatly condemn our success. Some dishonor we had in the loss of that drum, but it is not to be recover&#8217;d.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1309" number="17" form="prose">It might have been recover&#8217;d.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1310" number="18" form="prose">It might, but it is not now.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1311" number="19" form="prose">It is to be recover&#8217;d. But that the merit of service is seldom attributed to the true and exact performer, I would have that drum or another, or <foreign xml:lang="la">hic jacet</foreign>.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1312" number="20" form="prose">Why, if you have a stomach, to&#8217;t, <foreign xml:lang="fr">monsieur</foreign>: if you think your mystery in stratagem can bring this instrument of honor again into his native quarter, be magnanimious in the enterprise and go on; I will grace the attempt for a worthy exploit. If you speed well in it, the Duke shall both speak of it, and extend to you what further becomes his greatness, even to the utmost syllable of your worthiness.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1313" number="21" form="prose">By the hand of a soldier, I will undertake it.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1314" number="22" form="prose">But you must not now slumber in it.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1315" number="23" form="prose">I&#8217;ll about it this evening, and I will presently pen down my dilemmas, encourage myself in my certainty, put myself into my mortal preparation; and by midnight look to hear further from me.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1316" number="24" form="prose">May I be bold to acquaint his Grace you are gone about it?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1317" number="25" form="prose">I know not what the success will be, my lord, but the attempt I vow.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1318" number="26" form="prose">I know th&#8217; art valiant, and to the possibility of thy soldiership will subscribe for thee. Farewell.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1319" number="27" form="prose">I love not many words.</line>
</speech>

<stagedir sdglobalnumber="1319.01" sdnumber="27.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1320" number="28" form="prose">No more than a fish loves water. Is not this a strange fellow, my lord, that so confidently seems to undertake this business, which he knows is not to be done, damns himself to do, and dares better be damn&#8217;d than to do&#8217;t?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1321" number="29" form="prose">You do not know him, my lord, as we do. Certain it is that he will steal himself into a man&#8217;s favor, and for a week escape a great deal of discoveries, but when you find him out, you have him ever after.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1322" number="30" form="prose">Why, do you think he will make no deed at all of this that so seriously he does address himself unto?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1323" number="31" form="prose">None in the world, but return with an invention, and clap upon you two or three probable lies. But we have almost emboss&#8217;d him, you shall see his fall tonight; for indeed he is not for your lordship&#8217;s respect.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1324" number="32" form="prose">We&#8217;ll make you some sport with the fox ere we case him. He was first smok&#8217;d by the old Lord Lafew. When his disguise and he is parted, tell me what a sprat you shall find him, which you shall see this very night.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1325" number="33" form="verse">I must go look my twigs. He shall be caught.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1326" number="34" form="verse">Your brother he shall go along with me.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1327" number="35" form="verse">As&#8217;t please your lordship. I&#8217;ll leave you.</line>
</speech>

<stagedir sdglobalnumber="1327.01" sdnumber="35.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1328" number="36" form="verse">Now will I lead you to the house, and show you</line>
<line globalnumber="1329" number="37" form="verse" offset="0">The lass I spoke of.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1330" number="37" form="verse" offset="4">But you say she&#8217;s honest.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1331" number="38" form="verse">That&#8217;s all the fault. I spoke with her but once,</line>
<line globalnumber="1332" number="39" form="verse">And found her wondrous cold, but I sent to her,</line>
<line globalnumber="1333" number="40" form="verse">By this same coxcomb that we have i&#8217; th&#8217; wind,</line>
<line globalnumber="1334" number="41" form="verse">Tokens and letters which she did re-send,</line>
<line globalnumber="1335" number="42" form="verse">And this is all I have done. She&#8217;s a fair creature;</line>
<line globalnumber="1336" number="43" form="verse" offset="0">Will you go see her?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1337" number="43" form="verse" offset="4">With all my heart, my lord.</line>
</speech>

<stagedir sdglobalnumber="1337.01" sdnumber="43.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>BER.</actor>
		<actor>1. LORD. DUM.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="3" num="7">
<scenetitle>Scene 7</scenetitle>
<scenelocation>Florence. The Widow&#8217;s house.</scenelocation>

<scenepersonae>
	<scenepersona short="HEL.">Helen</scenepersona>
	<scenepersona short="WID.">Old Widow of Florence</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1337.02" sdnumber="0.01">
	<dir>Enter Helen and Widow.</dir>
	<action type="enter">
		<actor>HEL.</actor>
		<actor>WID.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1338" number="1" form="verse">If you misdoubt me that I am not she,</line>
<line globalnumber="1339" number="2" form="verse">I know not how I shall assure you further</line>
<line globalnumber="1340" number="3" form="verse">But I shall lose the grounds I work upon.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1341" number="4" form="verse">Though my estate be fall&#8217;n, I was well born,</line>
<line globalnumber="1342" number="5" form="verse">Nothing acquainted with these businesses,</line>
<line globalnumber="1343" number="6" form="verse">And would not put my reputation now</line>
<line globalnumber="1344" number="7" form="verse" offset="0">In any staining act.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1345" number="7" form="verse" offset="4">Nor would I wish you.</line>
<line globalnumber="1346" number="8" form="verse">First give me trust, the Count he is my husband,</line>
<line globalnumber="1347" number="9" form="verse">And what to your sworn counsel I have spoken</line>
<line globalnumber="1348" number="10" form="verse">Is so from word to word; and then you cannot,</line>
<line globalnumber="1349" number="11" form="verse">By the good aid that I of you shall borrow,</line>
<line globalnumber="1350" number="12" form="verse" offset="0">Err in bestowing it.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1351" number="12" form="verse" offset="4">I should believe you,</line>
<line globalnumber="1352" number="13" form="verse">For you have show&#8217;d me that which well approves</line>
<line globalnumber="1353" number="14" form="verse" offset="0">Y&#8217; are great in fortune.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1354" number="14" form="verse" offset="4">Take this purse of gold,</line>
<line globalnumber="1355" number="15" form="verse">And let me buy your friendly help thus far,</line>
<line globalnumber="1356" number="16" form="verse">Which I will over-pay and pay again</line>
<line globalnumber="1357" number="17" form="verse">When I have found it. The Count he woos your daughter,</line>
<line globalnumber="1358" number="18" form="verse">Lays down his wanton siege before her beauty,</line>
<line globalnumber="1359" number="19" form="verse">Resolv&#8217;d to carry her. Let her in fine consent,</line>
<line globalnumber="1360" number="20" form="verse">As we&#8217;ll direct her how &#8217;tis best to bear it.</line>
<line globalnumber="1361" number="21" form="verse">Now his important blood will nought deny</line>
<line globalnumber="1362" number="22" form="verse">That she&#8217;ll demand. A ring the County wears,</line>
<line globalnumber="1363" number="23" form="verse">That downward hath succeeded in his house</line>
<line globalnumber="1364" number="24" form="verse">From son to son, some four or five descents,</line>
<line globalnumber="1365" number="25" form="verse">Since the first father wore it. This ring he holds</line>
<line globalnumber="1366" number="26" form="verse">In most rich choice; yet in his idle fire,</line>
<line globalnumber="1367" number="27" form="verse">To buy his will, it would not seem too dear,</line>
<line globalnumber="1368" number="28" form="verse" offset="0">Howe&#8217;er repented after.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1369" number="28" form="verse" offset="5">Now I see</line>
<line globalnumber="1370" number="29" form="verse">The bottom of your purpose.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1371" number="30" form="verse">You see it lawful then. It is no more</line>
<line globalnumber="1372" number="31" form="verse">But that your daughter, ere she seems as won,</line>
<line globalnumber="1373" number="32" form="verse">Desires this ring; appoints him an encounter;</line>
<line globalnumber="1374" number="33" form="verse">In fine, delivers me to fill the time,</line>
<line globalnumber="1375" number="34" form="verse">Herself most chastely absent. After,</line>
<line globalnumber="1376" number="35" form="verse">To marry her, I&#8217;ll add three thousand crowns</line>
<line globalnumber="1377" number="36" form="verse" offset="0">To what is pass&#8217;d already.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1378" number="36" form="verse" offset="5">I have yielded.</line>
<line globalnumber="1379" number="37" form="verse">Instruct my daughter how she shall persever,</line>
<line globalnumber="1380" number="38" form="verse">That time and place with this deceit so lawful</line>
<line globalnumber="1381" number="39" form="verse">May prove coherent. Every night he comes</line>
<line globalnumber="1382" number="40" form="verse">With musics of all sorts, and songs compos&#8217;d</line>
<line globalnumber="1383" number="41" form="verse">To her unworthiness. It nothing steads us</line>
<line globalnumber="1384" number="42" form="verse">To chide him from our eaves, for he persists</line>
<line globalnumber="1385" number="43" form="verse" offset="0">As if his life lay on&#8217;t.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1386" number="43" form="verse" offset="4">Why then tonight</line>
<line globalnumber="1387" number="44" form="verse">Let us assay our plot, which if it speed,</line>
<line globalnumber="1388" number="45" form="verse">Is wicked meaning in a lawful deed,</line>
<line globalnumber="1389" number="46" form="verse">And lawful meaning in a lawful act,</line>
<line globalnumber="1390" number="47" form="verse">Where both not sin, and yet a sinful fact.</line>
<line globalnumber="1391" number="48" form="verse">But let&#8217;s about it.</line>
</speech>

<stagedir sdglobalnumber="1391.01" sdnumber="48.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>HEL.</actor>
		<actor>WID.</actor>
	</action>
</stagedir>

</scene>

</act>

<act num="4">
<acttitle>Act 4</acttitle>

<scene actnum="4" num="1">
<scenetitle>Scene 1</scenetitle>
<scenelocation>Without the Florentine camp.</scenelocation>

<scenepersonae>
	<scenepersona short="2. LORD. DUM.">Second French Lord</scenepersona>
	<scenepersona short="1. SOLD. AS INTERPRETER.">First Soldier as Interpreter</scenepersona>
	<scenepersona short="2. SOLD.">Second Soldier</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="">Gibberish</language>
</scenelanguage>


<stagedir sdglobalnumber="1391.02" sdnumber="0.01">
	<dir>Enter Second French Lord with five or six other Soldiers in ambush.</dir>
	<action type="enter">
		<actor>2. LORD. DUM.</actor>
		<actor>1. SOLD. AS INTERPRETER.</actor>
		<actor>2. SOLD.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1392" number="1" form="prose">He can come no other way but by this hedge-corner. When you sally upon him, speak what terrible language you will. Though you understand it not yourselves, no matter; for we must not seem to understand him, unless some one among us, whom we must produce for an interpreter.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1393" number="2" form="prose">Good captain, let me be th&#8217; interpreter.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1394" number="3" form="prose">Art not acquainted with him? Knows he not thy voice?</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1395" number="4" form="prose">No, sir, I warrant you.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1396" number="5" form="prose">But what linsey-woolsey hast thou to speak to us again?</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1397" number="6" form="prose">E&#8217;en such as you speak to me.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1398" number="7" form="prose">He must think us some band of strangers i&#8217; th&#8217; adversary&#8217;s entertainment. Now he hath a smack of all neighboring languages; therefore we must every one be a man of his own fancy, not to know what we speak one to another; so we seem to know, is to know straight our purpose: choughs&#8217; language, gabble enough, and good enough. As for you, interpreter, you must seem very politic. But couch ho, here he comes, to beguile two hours in a sleep, and then to return and swear the lies he forges.</line>
</speech>

<stagedir sdglobalnumber="1398.01" sdnumber="7.01">
	<dir>They stand aside.</dir>
	<action type="action">
		<actor>1. SOLD. AS INTERPRETER.</actor>
		<actor>2. LORD. DUM.</actor>
		<actor>2. SOLD.</actor>
	</action>
</stagedir>
<stagedir sdglobalnumber="1398.02" sdnumber="7.02">
	<dir>Enter Parolles.</dir>
	<action type="enter">
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech type="soliloquy">
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1399" number="8" form="prose">Ten a&#8217; clock: within these three hours &#8217;twill be time enough to go home. What shall I say I have done? It must be a very plausive invention that carries it. They begin to smoke me, and disgraces have of late knock&#8217;d too often at my door. I find my tongue is too foolhardy, but my heart hath the fear of Mars before it, and of his creatures, not daring the reports of my tongue.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<stagedir sdglobalnumber="1399.01" sdnumber="8.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="1400" number="9" form="prose">This is the first truth that e&#8217;er thine own tongue was guilty of.</line>
</speech>

<speech type="soliloquy">
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1401" number="10" form="prose">What the devil should move me to undertake the recovery of this drum, being not ignorant of the impossibility, and knowing I had no such purpose? I must give myself some hurts, and say I got them in exploit. Yet slight ones will not carry it. They will say, &#8220;Came you off with so little?&#8221; And great ones I dare not give; wherefore what&#8217;s the instance? Tongue, I must put you into a butter-woman&#8217;s mouth and buy myself another of Bajazeth&#8217;s mule, if you prattle me into these perils.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>

<stagedir sdglobalnumber="1401.01" sdnumber="10.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="1402" number="11" form="prose">Is it possible he should know what he is, and be that he is?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1403" number="12" form="prose">I would the cutting of my garments would serve the turn, or the breaking of my Spanish sword.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>

<stagedir sdglobalnumber="1403.01" sdnumber="12.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="1404" number="13" form="prose">We cannot afford you so.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1405" number="14" form="prose">Or the baring of my beard, and to say it was in stratagem.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>

<stagedir sdglobalnumber="1405.01" sdnumber="14.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="1406" number="15" form="prose">&#8217;Twould not do.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1407" number="16" form="prose">Or to drown my clothes, and say I was stripp&#8217;d.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>

<stagedir sdglobalnumber="1407.01" sdnumber="16.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="1408" number="17" form="prose">Hardly serve.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1409" number="18" form="prose">Though I swore I leapt from the window of the citadel&#8212;</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>

<stagedir sdglobalnumber="1409.01" sdnumber="18.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="1410" number="19" form="prose">How deep?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1411" number="20" form="prose">Thirty fathom.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>

<stagedir sdglobalnumber="1411.01" sdnumber="20.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="1412" number="21" form="prose">Three great oaths would scarce make that be believ&#8217;d.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1413" number="22" form="prose">I would I had any drum of the enemy&#8217;s. I would swear I recover&#8217;d it.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>

<stagedir sdglobalnumber="1413.01" sdnumber="22.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>
<line globalnumber="1414" number="23" form="prose">You shall hear one anon.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1415" number="24" form="prose">A drum now of the enemy&#8217;s&#8212;</line>
</speech>

<stagedir sdglobalnumber="1415.01" sdnumber="24.01">
	<dir>Alarum within.</dir>
	<action type="sound">
	</action>
</stagedir>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1416" number="25" form="prose"><foreign xml:lang="art">Throca movousus, cargo, cargo, cargo.</foreign></line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1417" number="26" form="prose">O, ransom, ransom!</line>
<stagedir sdglobalnumber="1417.01" sdnumber="26.01">
	<dir>They seize him.</dir>
	<action type="action">
		<actor>1. SOLD. AS INTERPRETER.</actor>
		<actor>2. LORD. DUM.</actor>
		<actor>2. SOLD.</actor>
		<recipient>PAR.</recipient>
	</action>
</stagedir>
<line globalnumber="1418" number="27" form="prose">Do not hide mine eyes.</line>
</speech>

<stagedir sdglobalnumber="1418.01" sdnumber="27.01">
	<dir>They blindfold him.</dir>
	<action type="action">
		<actor>1. SOLD. AS INTERPRETER.</actor>
		<actor>2. LORD. DUM.</actor>
		<actor>2. SOLD.</actor>
		<recipient>PAR.</recipient>
	</action>
</stagedir>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1419" number="28" form="prose"><foreign xml:lang="art">Boskos thromuldo boskos.</foreign></line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1420" number="29" form="verse">I know you are the Muskos&#8217; regiment,</line>
<line globalnumber="1421" number="30" form="verse">And I shall lose my life for want of language.</line>
<line globalnumber="1422" number="31" form="verse">If there be here German, or Dane, Low Dutch,</line>
<line globalnumber="1423" number="32" form="verse">Italian, or French, let him speak to me,</line>
<line globalnumber="1424" number="33" form="verse">I&#8217;ll discover that which shall undo the Florentine.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1425" number="34" form="prose"><foreign xml:lang="art">Boskos vauvado.</foreign> I understand thee, and can speak thy tongue. <foreign xml:lang="art">Kerelybonto</foreign>, sir, betake thee to thy faith, for seventeen poniards are at thy bosom.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1426" number="35" form="prose">O!</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1427" number="36" form="prose">O, pray, pray, pray! <foreign xml:lang="art">Manka revania dulche.</foreign></line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1428" number="37" form="prose"><foreign xml:lang="art">Oscorbidulchos volivorco.</foreign></line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1429" number="38" form="verse">The general is content to spare thee yet,</line>
<line globalnumber="1430" number="39" form="verse">And hoodwink&#8217;d as thou art, will lead thee on</line>
<line globalnumber="1431" number="40" form="verse">To gather from thee. Haply thou mayst inform</line>
<line globalnumber="1432" number="41" form="verse" offset="0">Something to save thy life.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1433" number="41" form="verse" offset="5">O, let me live,</line>
<line globalnumber="1434" number="42" form="verse">And all the secrets of our camp I&#8217;ll show,</line>
<line globalnumber="1435" number="43" form="verse">Their force, their purposes; nay, I&#8217;ll speak that</line>
<line globalnumber="1436" number="44" form="verse" offset="0">Which you will wonder at.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1437" number="44" form="verse" offset="5">But wilt thou faithfully?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1438" number="45" form="verse" offset="0">If I do not, damn me.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1439" number="45" form="verse" offset="4"><foreign xml:lang="art">Acordo linta.</foreign></line>
<line globalnumber="1440" number="46" form="verse">Come on, thou art granted space,</line>
</speech>

<stagedir sdglobalnumber="1440.01" sdnumber="46.01">
	<dir>Exit with Parolles guarded.</dir>
	<action type="exit">
		<actor>1. SOLD. AS INTERPRETER.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="1440.02" sdnumber="46.02">
	<dir>A short alarum within.</dir>
	<action type="sound">
	</action>
</stagedir>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1441" number="47" form="verse">Go tell the Count Roussillon, and my brother,</line>
<line globalnumber="1442" number="48" form="verse">We have caught the woodcock, and will keep him muffled</line>
<line globalnumber="1443" number="49" form="verse" offset="0">Till we do hear from them.</line>
</speech>

<speech>
<speaker long="Second Soldier">2. SOLD.</speaker>
<line globalnumber="1444" number="49" form="verse" offset="5">Captain, I will.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1445" number="50" form="verse">&#8217;A will betray us all unto ourselves:</line>
<line globalnumber="1446" number="51" form="verse" offset="0">Inform on that.</line>
</speech>

<speech>
<speaker long="Second Soldier">2. SOLD.</speaker>
<line globalnumber="1447" number="51" form="verse" offset="3">So I will, sir.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1448" number="52" form="verse">Till then I&#8217;ll keep him dark and safely lock&#8217;d.</line>
</speech>

<stagedir sdglobalnumber="1448.01" sdnumber="52.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>2. LORD. DUM.</actor>
		<actor>2. SOLD.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="4" num="2">
<scenetitle>Scene 2</scenetitle>
<scenelocation>Florence. The Widow&#8217;s house.</scenelocation>

<scenepersonae>
	<scenepersona short="BER.">Bertram</scenepersona>
	<scenepersona short="DIA.">Diana</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="fr">French</language>
</scenelanguage>


<stagedir sdglobalnumber="1448.02" sdnumber="0.01">
	<dir>Enter Bertram and the maid called Diana.</dir>
	<action type="enter">
		<actor>BER.</actor>
		<actor>DIA.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1449" number="1" form="verse">They told me that your name was Fontibell.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1450" number="2" form="verse" offset="0">No, my good lord, Diana.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1451" number="2" form="verse" offset="5">Titled goddess,</line>
<line globalnumber="1452" number="3" form="verse">And worth it, with addition! But, fair soul,</line>
<line globalnumber="1453" number="4" form="verse">In your fine frame hath love no quality?</line>
<line globalnumber="1454" number="5" form="verse">If the quick fire of youth light not your mind,</line>
<line globalnumber="1455" number="6" form="verse">You are no maiden, but a monument.</line>
<line globalnumber="1456" number="7" form="verse">When you are dead, you should be such a one</line>
<line globalnumber="1457" number="8" form="verse">As you are now; for you are cold and stern,</line>
<line globalnumber="1458" number="9" form="verse">And now you should be as your mother was</line>
<line globalnumber="1459" number="10" form="verse">When your sweet self was got.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1460" number="11" form="verse" offset="0">She then was honest.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1461" number="11" form="verse" offset="4">So should you be.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1462" number="11" form="verse" offset="8">No;</line>
<line globalnumber="1463" number="12" form="verse">My mother did but duty, such, my lord,</line>
<line globalnumber="1464" number="13" form="verse" offset="0">As you owe to your wife.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1465" number="13" form="verse" offset="5">No more a&#8217; that.</line>
<line globalnumber="1466" number="14" form="verse">I prithee do not strive against my vows.</line>
<line globalnumber="1467" number="15" form="verse">I was compell&#8217;d to her, but I love thee</line>
<line globalnumber="1468" number="16" form="verse">By love&#8217;s own sweet constraint, and will forever</line>
<line globalnumber="1469" number="17" form="verse" offset="0">Do thee all rights of service.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1470" number="17" form="verse" offset="6">Ay, so you serve us</line>
<line globalnumber="1471" number="18" form="verse">Till we serve you; but when you have our roses,</line>
<line globalnumber="1472" number="19" form="verse">You barely leave our thorns to prick ourselves,</line>
<line globalnumber="1473" number="20" form="verse" offset="0">And mock us with our bareness.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1474" number="20" form="verse" offset="7">How have I sworn!</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1475" number="21" form="verse">&#8217;Tis not the many oaths that makes the truth,</line>
<line globalnumber="1476" number="22" form="verse">But the plain single vow that is vow&#8217;d true.</line>
<line globalnumber="1477" number="23" form="verse">What is not holy, that we swear not by,</line>
<line globalnumber="1478" number="24" form="verse">But take the High&#8217;st to witness. Then pray you tell me,</line>
<line globalnumber="1479" number="25" form="verse">If I should swear by Jove&#8217;s great attributes</line>
<line globalnumber="1480" number="26" form="verse">I lov&#8217;d you dearly, would you believe my oaths</line>
<line globalnumber="1481" number="27" form="verse">When I did love you ill? This has no holding,</line>
<line globalnumber="1482" number="28" form="verse">To swear by Him whom I protest to love</line>
<line globalnumber="1483" number="29" form="verse">That I will work against Him; therefore your oaths</line>
<line globalnumber="1484" number="30" form="verse">Are words and poor conditions, but unseal&#8217;d&#8212;</line>
<line globalnumber="1485" number="31" form="verse" offset="0">At least in my opinion.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1486" number="31" form="verse" offset="5">Change it, change it!</line>
<line globalnumber="1487" number="32" form="verse">Be not so holy-cruel. Love is holy,</line>
<line globalnumber="1488" number="33" form="verse">And my integrity ne&#8217;er knew the crafts</line>
<line globalnumber="1489" number="34" form="verse">That you do charge men with. Stand no more off,</line>
<line globalnumber="1490" number="35" form="verse">But give thyself unto my sick desires,</line>
<line globalnumber="1491" number="36" form="verse">Who then recovers. Say thou art mine, and ever</line>
<line globalnumber="1492" number="37" form="verse">My love, as it begins, shall so persever.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1493" number="38" form="verse">I see that men make rope&#8217;s in such a scarre,</line>
<line globalnumber="1494" number="39" form="verse">That we&#8217;ll forsake ourselves. Give me that ring.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1495" number="40" form="verse">I&#8217;ll lend it thee, my dear; but have no power</line>
<line globalnumber="1496" number="41" form="verse" offset="0">To give it from me.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1497" number="41" form="verse" offset="4">Will you not, my lord?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1498" number="42" form="verse">It is an honor &#8217;longing to our house,</line>
<line globalnumber="1499" number="43" form="verse">Bequeathed down from many ancestors,</line>
<line globalnumber="1500" number="44" form="verse">Which were the greatest obloquy i&#8217; th&#8217; world</line>
<line globalnumber="1501" number="45" form="verse" offset="0">In me to lose.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1502" number="45" form="verse" offset="3">Mine honor&#8217;s such a ring,</line>
<line globalnumber="1503" number="46" form="verse">My chastity&#8217;s the jewel of our house,</line>
<line globalnumber="1504" number="47" form="verse">Bequeathed down from many ancestors,</line>
<line globalnumber="1505" number="48" form="verse">Which were the greatest obloquy i&#8217; th&#8217; world</line>
<line globalnumber="1506" number="49" form="verse">In me to lose. Thus your own proper wisdom</line>
<line globalnumber="1507" number="50" form="verse">Brings in the champion Honor on my part,</line>
<line globalnumber="1508" number="51" form="verse" offset="0">Against your vain assault.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1509" number="51" form="verse" offset="5">Here, take my ring!</line>
<line globalnumber="1510" number="52" form="verse">My house, mine honor, yea, my life, be thine,</line>
<line globalnumber="1511" number="53" form="verse">And I&#8217;ll be bid by thee.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1512" number="54" form="verse">When midnight comes, knock at my chamber-window;</line>
<line globalnumber="1513" number="55" form="verse">I&#8217;ll order take my mother shall not hear.</line>
<line globalnumber="1514" number="56" form="verse">Now will I charge you in the band of truth,</line>
<line globalnumber="1515" number="57" form="verse">When you have conquer&#8217;d my yet maiden bed,</line>
<line globalnumber="1516" number="58" form="verse">Remain there but an hour, nor speak to me.</line>
<line globalnumber="1517" number="59" form="verse">My reasons are most strong, and you shall know them</line>
<line globalnumber="1518" number="60" form="verse">When back again this ring shall be deliver&#8217;d;</line>
<line globalnumber="1519" number="61" form="verse">And on your finger in the night I&#8217;ll put</line>
<line globalnumber="1520" number="62" form="verse">Another ring, that what in time proceeds</line>
<line globalnumber="1521" number="63" form="verse">May token to the future our past deeds.</line>
<line globalnumber="1522" number="64" form="verse"><foreign xml:lang="fr">Adieu</foreign> till then, then fail not. You have won</line>
<line globalnumber="1523" number="65" form="verse">A wife of me, though there my hope be done.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1524" number="66" form="verse">A heaven on earth I have won by wooing thee.</line>
</speech>

<stagedir sdglobalnumber="1524.01" sdnumber="66.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>BER.</actor>
	</action>
</stagedir>

<speech type="soliloquy">
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1525" number="67" form="verse">For which live long to thank both heaven and me!</line>
<line globalnumber="1526" number="68" form="verse">You may so in the end.</line>
<line globalnumber="1527" number="69" form="verse">My mother told me just how he would woo,</line>
<line globalnumber="1528" number="70" form="verse">As if she sate in &#8217;s heart. She says all men</line>
<line globalnumber="1529" number="71" form="verse">Have the like oaths. He had sworn to marry me</line>
<line globalnumber="1530" number="72" form="verse">When his wife&#8217;s dead; therefore I&#8217;ll lie with him</line>
<line globalnumber="1531" number="73" form="verse">When I am buried. Since Frenchmen are so braid,</line>
<line globalnumber="1532" number="74" form="verse">Marry that will, I live and die a maid.</line>
<line globalnumber="1533" number="75" form="verse">Only in this disguise I think&#8217;t no sin</line>
<line globalnumber="1534" number="76" form="verse">To cozen him that would unjustly win.</line>
</speech>

<stagedir sdglobalnumber="1534.01" sdnumber="76.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>DIA.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="4" num="3">
<scenetitle>Scene 3</scenetitle>
<scenelocation>The Florentine camp.</scenelocation>

<scenepersonae>
	<scenepersona short="BOTH LORDS.">French Lords</scenepersona>
	<scenepersona short="1. SOLD. AS INTERPRETER.">First Soldier as Interpreter</scenepersona>
	<scenepersona short="2. SOLD.">Second Soldier</scenepersona>
	<scenepersona short="MESS.">Messenger</scenepersona>
	<scenepersona short="BER.">Bertram</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
    <language short="fr">French</language>
    <language short="">Gibberish</language>
</scenelanguage>


<stagedir sdglobalnumber="1534.02" sdnumber="0.01">
	<dir>Enter the two French Lords and some two or three Soldiers.</dir>
	<action type="enter">
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1535" number="1" form="prose">You have not given him his mother&#8217;s letter?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1536" number="2" form="prose">I have deliv&#8217;red it an hour since. There is something in&#8217;t that stings his nature; for on the reading it he chang&#8217;d almost into another man.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1537" number="3" form="prose">He has much worthy blame laid upon him for shaking off so good a wife and so sweet a lady.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1538" number="4" form="prose">Especially he hath incurr&#8217;d the everlasting displeasure of the King, who had even tun&#8217;d his bounty to sing happiness to him. I will tell you a thing, but you shall let it dwell darkly with you.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1539" number="5" form="prose">When you have spoken it, &#8217;tis dead, and I am the grave of it.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1540" number="6" form="prose">He hath perverted a young gentlewoman here in Florence, of a most chaste renown, and this night he fleshes his will in the spoil of her honor. He hath given her his monumental ring, and thinks himself made in the unchaste composition.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1541" number="7" form="prose">Now God delay our rebellion! As we are ourselves, what things are we!</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1542" number="8" form="prose">Merely our own traitors. And as in the common course of all treasons, we still see them reveal themselves, till they attain to their abhorr&#8217;d ends; so he that in this action contrives against his own nobility in his proper stream o&#8217;erflows himself.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1543" number="9" form="prose">Is it not meant damnable in us, to be trumpeters of our unlawful intents? We shall not then have his company tonight?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1544" number="10" form="prose">Not till after midnight; for he is dieted to his hour.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1545" number="11" form="prose">That approaches apace. I would gladly have him see his company anatomiz&#8217;d, that he might take a measure of his own judgments, wherein so curiously he had set this counterfeit.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1546" number="12" form="prose">We will not meddle with him till he come; for his presence must be the whip of the other.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1547" number="13" form="prose">In the meantime, what hear you of these wars?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1548" number="14" form="prose">I hear there is an overture of peace.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1549" number="15" form="prose">Nay, I assure you a peace concluded.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1550" number="16" form="prose">What will Count Roussillon do then? Will he travel higher, or return again into France?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1551" number="17" form="prose">I perceive by this demand, you are not altogether of his counsel.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1552" number="18" form="prose">Let it be forbid, sir, so should I be a great deal of his act.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1553" number="19" form="prose">Sir, his wife some two months since fled from his house. Her pretense is a pilgrimage to Saint Jaques le Grand; which holy undertaking with most austere sanctimony she accomplish&#8217;d; and there residing, the tenderness of her nature became as a prey to her grief; in fine, made a groan of her last breath, and now she sings in heaven.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1554" number="20" form="prose">How is this justified?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1555" number="21" form="prose">The stronger part of it by her own letters, which makes her story true, even to the point of her death. Her death itself, which could not be her office to say is come, was faithfully confirm&#8217;d by the rector of the place.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1556" number="22" form="prose">Hath the Count all this intelligence?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1557" number="23" form="prose">Ay, and the particular confirmations, point from point, to the full arming of the verity.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1558" number="24" form="prose">I am heartily sorry that he&#8217;ll be glad of this.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1559" number="25" form="prose">How mightily sometimes we make us comforts of our losses!</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1560" number="26" form="prose">And how mightily some other times we drown our gain in tears! The great dignity that his valor hath here acquir&#8217;d for him shall at home be encount&#8217;red with a shame as ample.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1561" number="27" form="prose">The web of our life is of a mingled yarn, good and ill together: our virtues would be proud, if our faults whipt them not, and our crimes would despair, if they were not cherish&#8217;d by our virtues.</line>
<stagedir sdglobalnumber="1561.01" sdnumber="27.01">
	<dir>Enter a Messenger.</dir>
	<action type="enter">
		<actor>MESS.</actor>
	</action>
</stagedir>
<line globalnumber="1562" number="28" form="prose">How now? Where&#8217;s your master?</line>
</speech>

<speech>
<speaker long="Messenger">MESS.</speaker>
<line globalnumber="1563" number="29" form="prose">He met the Duke in the street, sir, of whom he hath taken a solemn leave. His lordship will next morning for France. The Duke hath offer&#8217;d him letters of commendations to the King.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1564" number="30" form="prose">They shall be no more than needful there, if they were more than they can commend.</line>
</speech>

<stagedir sdglobalnumber="1564.01" sdnumber="30.01">
	<dir>Exit Messenger.</dir>
	<action type="exit">
		<actor>MESS.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="1564.02" sdnumber="30.02">
	<dir>Enter (Bertram) Count Roussillon.</dir>
	<action type="enter">
		<actor>BER.</actor>
	</action>
</stagedir>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1565" number="31" form="prose">They cannot be too sweet for the King&#8217;s tartness. Here&#8217;s his lordship now. How now, my lord, is&#8217;t not after midnight?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1566" number="32" form="prose">I have tonight dispatch&#8217;d sixteen businesses, a month&#8217;s length a-piece, by an abstract of success: I have congied with the Duke, done my <foreign xml:lang="fr">adieu</foreign> with his nearest; buried a wife, mourn&#8217;d for her, writ to my lady mother I am returning, entertain&#8217;d my convoy, and between these main parcels of dispatch effected many nicer needs. The last was the greatest, but that I have not ended yet.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1567" number="33" form="prose">If the business be of any difficulty, and this morning your departure hence, it requires haste of your lordship.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1568" number="34" form="prose">I mean the business is not ended, as fearing to hear of it hereafter. But shall we have this dialogue between the fool and the soldier? Come, bring forth this counterfeit module, h&#8217;as deceiv&#8217;d me like a double-meaning prophesier.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1569" number="35" form="prose">Bring him forth, h&#8217;as sate i&#8217; th&#8217; stocks all night, poor gallant knave.</line>
</speech>

<stagedir sdglobalnumber="1569.01" sdnumber="35.01">
	<dir>Exeunt Soldiers.</dir>
	<action type="exit">
	</action>
</stagedir>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1570" number="36" form="prose">No matter, his heels have deserv&#8217;d it, in usurping his spurs so long. How does he carry himself?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1571" number="37" form="prose">I have told your lordship already: the stocks carry him. But to answer you as you would be understood, he weeps like a wench that had shed her milk. He hath confess&#8217;d himself to Morgan, whom he supposes to be a friar, from the time of his remembrance to this very instant disaster of his setting i&#8217; th&#8217; stocks; and what think you he hath confess&#8217;d?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1572" number="38" form="prose">Nothing of me, has &#8217;a?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1573" number="39" form="prose">His confession is taken, and it shall be read to his face. If your lordship be in&#8217;t, as I believe you are, you must have the patience to hear it.</line>
</speech>

<stagedir sdglobalnumber="1573.01" sdnumber="39.01">
	<dir>Enter Soldiers and Parolles, with First Soldier as his Interpreter.</dir>
	<action type="enter">
		<actor>PAR.</actor>
		<actor>1. SOLD. AS INTERPRETER.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1574" number="40" form="prose">A plague upon him! Muffled! He can say nothing of me.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1575" number="41" form="prose">Hush, hush! Hoodman comes! <foreign xml:lang="art">Portotartarossa.</foreign></line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1576" number="42" form="prose">He calls for the tortures. What will you say without &#8217;em?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1577" number="43" form="prose">I will confess what I know without constraint. If ye pinch me like a pasty, I can say no more.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1578" number="44" form="prose"><foreign xml:lang="art">Bosko chimurcho.</foreign></line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1579" number="45" form="prose"><foreign xml:lang="art">Boblibindo chicurmurco.</foreign></line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1580" number="46" form="prose">You are a merciful general. Our general bids you answer to what I shall ask you out of a note.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1581" number="47" form="prose">And truly, as I hope to live.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>

<stagedir sdglobalnumber="1581.01" sdnumber="47.01">
	<dir>Reads.</dir>
	<action type="read">
		<actor>1. SOLD. AS INTERPRETER.</actor>
	</action>
</stagedir>
<line globalnumber="1582" number="48" form="prose"><recite>&#8220;First demand of him, how many horse the Duke is strong.&#8221;</recite><lb />What say you to that?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1583" number="49" form="prose">Five or six thousand, but very weak and unserviceable. The troops are all scatter&#8217;d, and the commanders very poor rogues, upon my reputation and credit and as I hope to live.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1584" number="50" form="prose">Shall I set down your answer so?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1585" number="51" form="prose">Do, I&#8217;ll take the sacrament on&#8217;t, how and which way you will.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1586" number="52" form="prose">All&#8217;s one to him. What a past-saving slave is this!</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1587" number="53" form="prose">Y&#8217; are deceiv&#8217;d, my lord, this is <foreign xml:lang="fr">Monsieur</foreign> Parolles, the gallant militarist&#8212;that was his own phrase&#8212;that had the whole theoric of war in the knot of his scarf, and the practice in the chape of his dagger.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1588" number="54" form="prose">I will never trust a man again for keeping his sword clean, nor believe he can have every thing in him by wearing his apparel neatly.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1589" number="55" form="prose">Well, that&#8217;s set down.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1590" number="56" form="prose">&#8220;Five or six thousand horse,&#8221; I said&#8212;I will say true&#8212; &#8220;or thereabouts,&#8221; set down, for I&#8217;ll speak truth.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1591" number="57" form="prose">He&#8217;s very near the truth in this.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1592" number="58" form="prose">But I con him no thanks for&#8217;t, in the nature he delivers it.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1593" number="59" form="prose">&#8220;Poor rogues,&#8221; I pray you say.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1594" number="60" form="prose">Well, that&#8217;s set down.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1595" number="61" form="prose">I humbly thank you, sir. A truth&#8217;s a truth, the rogues are marvelous poor.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>

<stagedir sdglobalnumber="1595.01" sdnumber="61.01">
	<dir>Reads.</dir>
	<action type="read">
		<actor>1. SOLD. AS INTERPRETER.</actor>
	</action>
</stagedir>
<line globalnumber="1596" number="62" form="prose"><recite>&#8220;Demand of him, of what strength they are afoot.&#8221;</recite><lb />What say you to that?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1597" number="63" form="prose">By my troth, sir, if I were to live this present hour, I will tell true. Let me see: Spurio, a hundred and fifty; Sebastian, so many; Corambus, so many; Jaques, so many; Guiltian, Cosmo, Lodowick, and Gratii, two hundred fifty each; mine own company, Chitopher, Vaumond, Bentii, two hundred fifty each; so that the muster-file, rotten and sound, upon my life, amounts not to fifteen thousand pole, half of the which dare not shake the snow from off their cassocks, lest they shake themselves to pieces.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1598" number="64" form="prose">What shall be done to him?</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1599" number="65" form="prose">Nothing, but let him have thanks. Demand of him my condition, and what credit I have with the Duke.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1600" number="66" form="prose">Well, that&#8217;s set down.</line>
<stagedir sdglobalnumber="1600.01" sdnumber="66.01">
	<dir>Reads.</dir>
	<action type="read">
		<actor>1. SOLD. AS INTERPRETER.</actor>
	</action>
</stagedir>
<line globalnumber="1601" number="67" form="prose"><recite>&#8220;You shall demand of him, whether one Captain Dumaine be i&#8217; th&#8217; camp, a Frenchman; what his reputation is with the Duke; what his valor, honesty, and expertness in wars; or whether he thinks it were not possible with well-weighing sums of gold to corrupt him to a revolt.&#8221;</recite><lb />What say you to this? What do you know of it?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1602" number="68" form="prose">I beseech you let me answer to the particular of the inter&#8217;gatories. Demand them singly.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1603" number="69" form="prose">Do you know this Captain Dumaine?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1604" number="70" form="prose">I know him. &#8217;A was a botcher&#8217;s prentice in Paris, from whence he was whipt for getting the shrieve&#8217;s fool with child, a dumb innocent, that could not say him nay.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1605" number="71" form="prose">Nay, by your leave, hold your hands&#8212;though I know his brains are forfeit to the next tile that falls.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1606" number="72" form="prose">Well, is this captain in the Duke of Florence&#8217;s camp?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1607" number="73" form="prose">Upon my knowledge, he is, and lousy.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1608" number="74" form="prose">Nay, look not so upon me; we shall hear of your lordship anon.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1609" number="75" form="prose">What is his reputation with the Duke?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1610" number="76" form="prose">The Duke knows him for no other but a poor officer of mine, and writ to me this other day to turn him out a&#8217; th&#8217; band. I think I have his letter in my pocket.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1611" number="77" form="prose">Marry, we&#8217;ll search.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1612" number="78" form="prose">In good sadness, I do not know. Either it is there, or it is upon a file with the Duke&#8217;s other letters in my tent.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1613" number="79" form="prose">Here &#8217;tis, here&#8217;s a paper. Shall I read it to you?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1614" number="80" form="prose">I do not know if it be it or no.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1615" number="81" form="prose">Our interpreter does it well.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1616" number="82" form="prose">Excellently.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<stagedir sdglobalnumber="1616.01" sdnumber="82.01">
	<dir>Reads.</dir>
	<action type="read">
		<actor>1. SOLD. AS INTERPRETER.</actor>
	</action>
</stagedir>
<line globalnumber="1617" number="83" form="verse"><recite>&#8220;Dian, the Count&#8217;s a fool, and full of gold&#8221;&#8212;</recite></line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1618" number="84" form="prose">That is not the Duke&#8217;s letter, sir; that is an advertisement to a proper maid in Florence, one Diana, to take heed of the allurement of one Count Roussillon, a foolish idle boy, but for all that very ruttish. I pray you, sir, put it up again.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1619" number="85" form="prose">Nay, I&#8217;ll read it first, by your favor.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1620" number="86" form="prose">My meaning in&#8217;t, I protest, was very honest in the behalf of the maid; for I knew the young Count to be a dangerous and lascivious boy, who is a whale to virginity, and devours up all the fry it finds.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1621" number="87" form="prose">Damnable both-sides rogue!</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<stagedir sdglobalnumber="1621.01" sdnumber="87.01">
	<dir>Reads the letter.</dir>
	<action type="read">
		<actor>1. SOLD. AS INTERPRETER.</actor>
	</action>
</stagedir>
<line globalnumber="1622" number="88" form="verse"><recite>&#8220;When he swears oaths, bid him drop gold, and take it;</recite></line>
<line globalnumber="1623" number="89" form="verse"><recite>After he scores, he never pays the score.</recite></line>
<line globalnumber="1624" number="90" form="verse"><recite>Half won is match well made; match, and well make it;</recite></line>
<line globalnumber="1625" number="91" form="verse"><recite>He ne&#8217;er pays after-debts, take it before,</recite></line>
<line globalnumber="1626" number="92" form="verse"><recite>And say a soldier, Dian, told thee this:</recite></line>
<line globalnumber="1627" number="93" form="verse"><recite>Men are to mell with, boys are not to kiss;</recite></line>
<line globalnumber="1628" number="94" form="verse"><recite>For count of this, the Count&#8217;s a fool, I know it,</recite></line>
<line globalnumber="1629" number="95" form="verse"><recite>Who pays before, but not when he does owe it.</recite></line>
<line globalnumber="1630" number="96" form="verse"><recite>Thine, as he vow&#8217;d to thee in thine ear,</recite></line>
<line globalnumber="1631" number="97" form="verse"><recite>Parolles.&#8221;</recite></line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1632" number="98" form="prose">He shall be whipt through the army with this rhyme in &#8217;s forehead.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1633" number="99" form="prose">This is your devoted friend, sir, the manifold linguist and the armipotent soldier.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1634" number="100" form="prose">I could endure any thing before but a cat, and now he&#8217;s a cat to me.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1635" number="101" form="prose">I perceive, sir, by the general&#8217;s looks, we shall be fain to hang you.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1636" number="102" form="prose">My life, sir, in any case! Not that I am afraid to die, but that my offenses being many, I would repent out the remainder of nature. Let me live, sir, in a dungeon, i&#8217; th&#8217; stocks, or any where, so I may live.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1637" number="103" form="prose">We&#8217;ll see what may be done, so you confess freely; therefore once more to this Captain Dumaine. You have answer&#8217;d to his reputation with the Duke, and to his valor; what is his honesty?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1638" number="104" form="prose">He will steal, sir, an egg out of a cloister. For rapes and ravishments he parallels Nessus. He professes not keeping of oaths; in breaking &#8217;em he is stronger than Hercules. He will lie, sir, with such volubility, that you would think truth were a fool. Drunkenness is his best virtue, for he will be swine-drunk, and in his sleep he does little harm, save to his bed-clothes about him; but they know his conditions, and lay him in straw. I have but little more to say, sir, of his honesty. He has every thing that an honest man should not have; what an honest man should have, he has nothing.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1639" number="105" form="prose">I begin to love him for this.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1640" number="106" form="prose">For this description of thine honesty? A pox upon him for me, he&#8217;s more and more a cat.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1641" number="107" form="prose">What say you to his expertness in war?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1642" number="108" form="prose">Faith, sir, h&#8217;as led the drum before the English tragedians. To belie him I will not, and more of his soldiership I know not, except in that country he had the honor to be the officer at a place there call&#8217;d Mile-end, to instruct for the doubling of files. I would do the man what honor I can, but of this I am not certain.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1643" number="109" form="prose">He hath out-villain&#8217;d villainy so far, that the rarity redeems him.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1644" number="110" form="prose">A pox on him, he&#8217;s a cat still.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1645" number="111" form="prose">His qualities being at this poor price, I need not to ask you if gold will corrupt him to revolt.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1646" number="112" form="prose">Sir, for a cardecue he will sell the fee-simple of his salvation, the inheritance of it, and cut th&#8217; entail from all remainders, and a perpetual succession for it perpetually.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1647" number="113" form="prose">What&#8217;s his brother, the other Captain Dumaine?</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1648" number="114" form="prose">Why does he ask him of me?</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1649" number="115" form="prose">What&#8217;s he?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1650" number="116" form="prose">E&#8217;en a crow a&#8217; th&#8217; same nest; not altogether so great as the first in goodness, but greater a great deal in evil. He excels his brother for a coward, yet his brother is reputed one of the best that is. In a retreat he outruns any lackey; marry, in coming on he has the cramp.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1651" number="117" form="prose">If your life be sav&#8217;d, will you undertake to betray the Florentine?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1652" number="118" form="prose">Ay, and the captain of his horse, Count Roussillon.</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1653" number="119" form="prose">I&#8217;ll whisper with the general, and know his pleasure.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>

<stagedir sdglobalnumber="1653.01" sdnumber="119.01">
	<dir>Aside.</dir>
	<action type="aside">
		<actor>PAR.</actor>
	</action>
</stagedir>
<line globalnumber="1654" number="120" form="prose">I&#8217;ll no more drumming, a plague of all drums! Only to seem to deserve well, and to beguile the supposition of that lascivious young boy the Count, have I run into this danger. Yet who would have suspected an ambush where I was taken?</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1655" number="121" form="prose">There is no remedy, sir, but you must die. The general says, you that have so traitorously discover&#8217;d the secrets of your army, and made such pestiferous reports of men very nobly held, can serve the world for no honest use; therefore you must die. Come, headsman, off with his head.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1656" number="122" form="prose">O Lord, sir, let me live, or let me see my death!</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1657" number="123" form="prose">That shall you, and take your leave of all your friends.</line>
<stagedir sdglobalnumber="1657.01" sdnumber="123.01">
	<dir>Unblinding him.</dir>
	<action type="action">
		<actor>1. SOLD. AS INTERPRETER.</actor>
		<recipient>PAR.</recipient>
	</action>
</stagedir>
<line globalnumber="1658" number="124" form="prose">So, look about you. Know you any here?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1659" number="125" form="prose">Good morrow, noble captain.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1660" number="126" form="prose">God bless you, Captain Parolles.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1661" number="127" form="prose">God save you, noble captain.</line>
</speech>

<speech>
<speaker long="Second French Lord Dumaine">2. LORD. DUM.</speaker>
<line globalnumber="1662" number="128" form="prose">Captain, what greeting will you to my Lord Lafew? I am for France.</line>
</speech>

<speech>
<speaker long="First French Lord Dumaine">1. LORD. DUM.</speaker>
<line globalnumber="1663" number="129" form="prose">Good captain, will you give me a copy of the sonnet you writ to Diana in behalf of the Count Roussillon? And I were not a very coward, I&#8217;d compel it of you, but fare you well.</line>
</speech>

<stagedir sdglobalnumber="1663.01" sdnumber="129.01">
	<dir>Exeunt Bertram and Lords.</dir>
	<action type="exit">
		<actor>BER.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
	</action>
</stagedir>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1664" number="130" form="prose">You are undone, captain, all but your scarf; that has a knot on&#8217;t yet.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1665" number="131" form="prose">Who cannot be crush&#8217;d with a plot?</line>
</speech>

<speech>
<speaker long="First Soldier as Interpreter">1. SOLD. AS INTERPRETER.</speaker>
<line globalnumber="1666" number="132" form="prose">If you could find out a country where but women were that had receiv&#8217;d so much shame, you might begin an impudent nation. Fare ye well, sir, I am for France too. We shall speak of you there.</line>
</speech>

<stagedir sdglobalnumber="1666.01" sdnumber="132.01">
	<dir>Exit with Soldiers.</dir>
	<action type="exit">
		<actor>1. SOLD. AS INTERPRETER.</actor>
	</action>
</stagedir>

<speech type="soliloquy">
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1667" number="133" form="verse">Yet am I thankful. If my heart were great,</line>
<line globalnumber="1668" number="134" form="verse">&#8217;Twould burst at this. Captain I&#8217;ll be no more,</line>
<line globalnumber="1669" number="135" form="verse">But I will eat and drink, and sleep as soft</line>
<line globalnumber="1670" number="136" form="verse">As captain shall. Simply the thing I am</line>
<line globalnumber="1671" number="137" form="verse">Shall make me live. Who knows himself a braggart,</line>
<line globalnumber="1672" number="138" form="verse">Let him fear this; for it will come to pass</line>
<line globalnumber="1673" number="139" form="verse">That every braggart shall be found an ass.</line>
<line globalnumber="1674" number="140" form="verse">Rust sword, cool blushes, and, Parolles, live</line>
<line globalnumber="1675" number="141" form="verse">Safest in shame! Being fool&#8217;d, by fool&#8217;ry thrive!</line>
<line globalnumber="1676" number="142" form="verse">There&#8217;s place and means for every man alive.</line>
<line globalnumber="1677" number="143" form="verse">I&#8217;ll after them.</line>
</speech>

<stagedir sdglobalnumber="1677.01" sdnumber="143.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>PAR.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="4" num="4">
<scenetitle>Scene 4</scenetitle>
<scenelocation>Florence. The Widow&#8217;s house.</scenelocation>

<scenepersonae>
	<scenepersona short="HEL.">Helen</scenepersona>
	<scenepersona short="WID.">Old Widow of Florence</scenepersona>
	<scenepersona short="DIA.">Diana</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1677.02" sdnumber="0.01">
	<dir>Enter Helen, Widow, and Diana.</dir>
	<action type="enter">
		<actor>HEL.</actor>
		<actor>WID.</actor>
		<actor>DIA.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1678" number="1" form="verse">That you may well perceive I have not wrong&#8217;d you,</line>
<line globalnumber="1679" number="2" form="verse">One of the greatest in the Christian world</line>
<line globalnumber="1680" number="3" form="verse">Shall be my surety; &#8217;fore whose throne &#8217;tis needful,</line>
<line globalnumber="1681" number="4" form="verse">Ere I can perfect mine intents, to kneel.</line>
<line globalnumber="1682" number="5" form="verse">Time was, I did him a desired office,</line>
<line globalnumber="1683" number="6" form="verse">Dear almost as his life, which gratitude</line>
<line globalnumber="1684" number="7" form="verse">Through flinty Tartar&#8217;s bosom would peep forth,</line>
<line globalnumber="1685" number="8" form="verse">And answer thanks. I duly am inform&#8217;d</line>
<line globalnumber="1686" number="9" form="verse">His Grace is at Marsellis, to which place</line>
<line globalnumber="1687" number="10" form="verse">We have convenient convoy. You must know</line>
<line globalnumber="1688" number="11" form="verse">I am supposed dead. The army breaking,</line>
<line globalnumber="1689" number="12" form="verse">My husband hies him home, where heaven aiding,</line>
<line globalnumber="1690" number="13" form="verse">And by the leave of my good lord the King,</line>
<line globalnumber="1691" number="14" form="verse" offset="0">We&#8217;ll be before our welcome.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1692" number="14" form="verse" offset="6">Gentle madam,</line>
<line globalnumber="1693" number="15" form="verse">You never had a servant to whose trust</line>
<line globalnumber="1694" number="16" form="verse" offset="0">Your business was more welcome.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1695" number="16" form="verse" offset="7">Nor you, mistress,</line>
<line globalnumber="1696" number="17" form="verse">Ever a friend whose thoughts more truly labor</line>
<line globalnumber="1697" number="18" form="verse">To recompense your love. Doubt not but heaven</line>
<line globalnumber="1698" number="19" form="verse">Hath brought me up to be your daughter&#8217;s dower,</line>
<line globalnumber="1699" number="20" form="verse">As it hath fated her to be my motive</line>
<line globalnumber="1700" number="21" form="verse">And helper to a husband. But O, strange men,</line>
<line globalnumber="1701" number="22" form="verse">That can such sweet use make of what they hate,</line>
<line globalnumber="1702" number="23" form="verse">When saucy trusting of the cozen&#8217;d thoughts</line>
<line globalnumber="1703" number="24" form="verse">Defiles the pitchy night; so lust doth play</line>
<line globalnumber="1704" number="25" form="verse">With what it loathes for that which is away&#8212;</line>
<line globalnumber="1705" number="26" form="verse">But more of this hereafter. You, Diana,</line>
<line globalnumber="1706" number="27" form="verse">Under my poor instructions yet must suffer</line>
<line globalnumber="1707" number="28" form="verse" offset="0">Something in my behalf.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1708" number="28" form="verse" offset="5">Let death and honesty</line>
<line globalnumber="1709" number="29" form="verse">Go with your impositions, I am yours</line>
<line globalnumber="1710" number="30" form="verse" offset="0">Upon your will to suffer.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1711" number="30" form="verse" offset="5">Yet, I pray you:</line>
<line globalnumber="1712" number="31" form="verse">But with the word the time will bring on summer,</line>
<line globalnumber="1713" number="32" form="verse">When briers shall have leaves as well as thorns,</line>
<line globalnumber="1714" number="33" form="verse">And be as sweet as sharp. We must away:</line>
<line globalnumber="1715" number="34" form="verse">Our wagon is prepar&#8217;d, and time revives us.</line>
<line globalnumber="1716" number="35" form="verse">All&#8217;s well that ends well! Still the fine&#8217;s the crown;</line>
<line globalnumber="1717" number="36" form="verse">What e&#8217;er the course, the end is the renown.</line>
</speech>

<stagedir sdglobalnumber="1717.01" sdnumber="36.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>HEL.</actor>
		<actor>WID.</actor>
		<actor>DIA.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="4" num="5">
<scenetitle>Scene 5</scenetitle>
<scenelocation>Roussillon. The Count&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="CLO.">Clown</scenepersona>
	<scenepersona short="COUNT.">Countess of Roussillon</scenepersona>
	<scenepersona short="LAF.">Lafew</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1717.02" sdnumber="0.01">
	<dir>Enter Clown, old Lady Countess, and Lafew.</dir>
	<action type="enter">
		<actor>LAF.</actor>
		<actor>COUNT.</actor>
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1718" number="1" form="prose">No, no, no, your son was misled with a snipt-taffeta fellow there, whose villainous saffron would have made all the unbak&#8217;d and doughy youth of a nation in his color. Your daughter-in-law had been alive at this hour, and your son here at home, more advanc&#8217;d by the King than by that red-tail&#8217;d humble-bee I speak of.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1719" number="2" form="prose">I would I had not known him; it was the death of the most virtuous gentlewoman that ever nature had praise for creating. If she had partaken of my flesh, and cost me the dearest groans of a mother, I could not have ow&#8217;d her a more rooted love.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1720" number="3" form="prose">&#8217;Twas a good lady, &#8217;twas a good lady. We may pick a thousand salads ere we light on such another herb.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1721" number="4" form="prose">Indeed, sir, she was the sweet marjoram of the salad, or rather the herb of grace.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1722" number="5" form="prose">They are not herbs, you knave, they are nose-herbs.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1723" number="6" form="prose">I am no great
Nebuchadnezzar, sir, I have not much skill in grass.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1724" number="7" form="prose">Whether dost thou profess thyself&#8212;a knave or a fool?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1725" number="8" form="prose">A fool, sir, at a woman&#8217;s service, and a knave at a man&#8217;s.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1726" number="9" form="prose">Your distinction?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1727" number="10" form="prose">I would cozen the man of his wife and do his service.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1728" number="11" form="prose">So you were a knave at his service indeed.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1729" number="12" form="prose">And I would give his wife my bauble, sir, to do her service.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1730" number="13" form="prose">I will subscribe for thee, thou art both knave and fool.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1731" number="14" form="prose">At your service.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1732" number="15" form="prose">No, no, no.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1733" number="16" form="prose">Why, sir, if I cannot serve you, I can serve as great a prince as you are.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1734" number="17" form="prose">Who&#8217;s that? A Frenchman?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1735" number="18" form="prose">Faith, sir, &#8217;a has an English name, but his fisnomy is more hotter in France than there.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1736" number="19" form="prose">What prince is that?</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1737" number="20" form="prose">The black prince, sir, alias the prince of darkness, alias the devil.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1738" number="21" form="prose">Hold thee, there&#8217;s my purse. I give thee not this to suggest thee from thy master thou talk&#8217;st of; serve him still.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1739" number="22" form="prose">I am a woodland fellow, sir, that always lov&#8217;d a great fire, and the master I speak of ever keeps a good fire. But sure he is the prince of the world; let his nobility remain in &#8217;s court. I am for the house with the narrow gate, which I take to be too little for pomp to enter. Some that humble themselves may, but the many will be too chill and tender, and they&#8217;ll be for the flow&#8217;ry way that leads to the broad gate and the great fire.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1740" number="23" form="prose">Go thy ways, I begin to be a-weary of thee, and I tell thee so before, because I would not fall out with thee. Go thy ways, let my horses be well look&#8217;d to, without any tricks.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1741" number="24" form="prose">If I put any tricks upon &#8217;em, sir, they shall be jades&#8217; tricks, which are their own right by the law of nature.</line>
</speech>

<stagedir sdglobalnumber="1741.01" sdnumber="24.01">
	<dir>Exit Clown.</dir>
	<action type="exit">
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1742" number="25" form="prose">A shrewd knave and an unhappy.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1743" number="26" form="prose">So &#8217;a is. My lord that&#8217;s gone made himself much sport out of him. By his authority he remains here, which he thinks is a patent for his sauciness, and indeed he has no pace, but runs where he will.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1744" number="27" form="prose">I like him well, &#8217;tis not amiss. And I was about to tell you, since I heard of the good lady&#8217;s death, and that my lord your son was upon his return home, I mov&#8217;d the King my master to speak in the behalf of my daughter, which in the minority of them both, his Majesty, out of a self-gracious remembrance, did first propose. His Highness hath promis&#8217;d me to do it, and to stop up the displeasure he hath conceiv&#8217;d against your son, there is no fitter matter. How does your ladyship like it?</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1745" number="28" form="prose">With very much content, my lord, and I wish it happily effected.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1746" number="29" form="prose">His Highness comes post from Marsellis, of as able body as when he number&#8217;d thirty. &#8217;A will be here tomorrow, or I am deceiv&#8217;d by him that in such intelligence hath seldom fail&#8217;d.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1747" number="30" form="prose">It rejoices me, that I hope I shall see him ere I die. I have letters that my son will be here tonight. I shall beseech your lordship to remain with me till they meet together.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1748" number="31" form="prose">Madam, I was thinking with what manners I might safely be admitted.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1749" number="32" form="prose">You need but plead your honorable privilege.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1750" number="33" form="prose">Lady, of that I have made a bold charter, but I thank my God it holds yet.</line>
</speech>

<stagedir sdglobalnumber="1750.01" sdnumber="33.01">
	<dir>Enter Clown.</dir>
	<action type="enter">
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1751" number="34" form="prose">O madam, yonder&#8217;s my lord your son with a patch of velvet on &#8217;s face. Whether there be a scar under&#8217;t or no, the velvet knows, but &#8217;tis a goodly patch of velvet. His left cheek is a cheek of two pile and a half, but his right cheek is worn bare.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1752" number="35" form="prose">A scar nobly got, or a noble scar, is a good liv&#8217;ry of honor; so belike is that.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1753" number="36" form="prose">But it is your carbinado&#8217;d face.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1754" number="37" form="prose">Let us go see your son I pray you. I long to talk with the young noble soldier.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1755" number="38" form="prose">Faith, there&#8217;s a dozen of &#8217;em, with delicate fine hats, and most courteous feathers, which bow the head, and nod at every man.</line>
</speech>

<stagedir sdglobalnumber="1755.01" sdnumber="38.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>LAF.</actor>
		<actor>COUNT.</actor>
		<actor>CLO.</actor>
	</action>
</stagedir>

</scene>

</act>

<act num="5">
<acttitle>Act 5</acttitle>

<scene actnum="5" num="1">
<scenetitle>Scene 1</scenetitle>
<scenelocation>Marseilles. A street.</scenelocation>

<scenepersonae>
	<scenepersona short="HEL.">Helen</scenepersona>
	<scenepersona short="WID.">Old Widow of Florence</scenepersona>
	<scenepersona short="DIA.">Diana</scenepersona>
	<scenepersona>Attendants</scenepersona>
	<scenepersona short="GENT.">Gentleman</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1755.02" sdnumber="0.01">
	<dir>Enter Helen, Widow, and Diana, with two Attendants.</dir>
	<action type="enter">
		<actor>HEL.</actor>
		<actor>WID.</actor>
		<actor>DIA.</actor>
		<actor>Attendants</actor>
	</action>
</stagedir>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1756" number="1" form="verse">But this exceeding posting day and night</line>
<line globalnumber="1757" number="2" form="verse">Must wear your spirits low; we cannot help it.</line>
<line globalnumber="1758" number="3" form="verse">But since you have made the days and nights as one,</line>
<line globalnumber="1759" number="4" form="verse">To wear your gentle limbs in my affairs,</line>
<line globalnumber="1760" number="5" form="verse">Be bold you do so grow in my requital</line>
<line globalnumber="1761" number="6" form="verse" offset="0">As nothing can unroot you.</line>
<stagedir sdglobalnumber="1761.01" sdnumber="6.01">
	<dir>Enter a Gentleman, an astringer.</dir>
	<action type="enter">
		<actor>GENT.</actor>
	</action>
</stagedir>
<line globalnumber="1762" number="6" form="verse" offset="6">In happy time!</line>
<line globalnumber="1763" number="7" form="verse">This man may help me to his Majesty&#8217;s ear,</line>
<line globalnumber="1764" number="8" form="verse">If he would spend his power. God save you, sir.</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1765" number="9" form="verse">And you.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1766" number="10" form="verse">Sir, I have seen you in the court of France.</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1767" number="11" form="verse">I have been sometimes there.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1768" number="12" form="verse">I do presume, sir, that you are not fall&#8217;n</line>
<line globalnumber="1769" number="13" form="verse">From the report that goes upon your goodness,</line>
<line globalnumber="1770" number="14" form="verse">And therefore goaded with most sharp occasions,</line>
<line globalnumber="1771" number="15" form="verse">Which lay nice manners by, I put you to</line>
<line globalnumber="1772" number="16" form="verse">The use of your own virtues, for the which</line>
<line globalnumber="1773" number="17" form="verse" offset="0">I shall continue thankful.</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1774" number="17" form="verse" offset="5">What&#8217;s your will?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1775" number="18" form="verse">That it will please you</line>
<line globalnumber="1776" number="19" form="verse">To give this poor petition to the King,</line>
<line globalnumber="1777" number="20" form="verse">And aid me with that store of power you have</line>
<line globalnumber="1778" number="21" form="verse">To come into his presence.</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1779" number="22" form="verse" offset="0">The King&#8217;s not here.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1780" number="22" form="verse" offset="4">Not here, sir?</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1781" number="22" form="verse" offset="8">Not indeed.</line>
<line globalnumber="1782" number="23" form="verse">He hence remov&#8217;d last night, and with more haste</line>
<line globalnumber="1783" number="24" form="verse" offset="0">Than is his use.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1784" number="24" form="verse" offset="4">Lord, how we lose our pains!</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1785" number="25" form="verse">All&#8217;s well that ends well yet,</line>
<line globalnumber="1786" number="26" form="verse">Though time seem so adverse and means unfit.</line>
<line globalnumber="1787" number="27" form="verse">I do beseech you, whither is he gone?</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1788" number="28" form="verse">Marry, as I take it, to Roussillon,</line>
<line globalnumber="1789" number="29" form="verse" offset="0">Whither I am going.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1790" number="29" form="verse" offset="4">I do beseech you, sir,</line>
<line globalnumber="1791" number="30" form="verse">Since you are like to see the King before me,</line>
<line globalnumber="1792" number="31" form="verse">Commend the paper to his gracious hand,</line>
<line globalnumber="1793" number="32" form="verse">Which I presume shall render you no blame,</line>
<line globalnumber="1794" number="33" form="verse">But rather make you thank your pains for it.</line>
<line globalnumber="1795" number="34" form="verse">I will come after you with what good speed</line>
<line globalnumber="1796" number="35" form="verse" offset="0">Our means will make us means.</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1797" number="35" form="verse" offset="7">This I&#8217;ll do for you.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="1798" number="36" form="verse">And you shall find yourself to be well thank&#8217;d,</line>
<line globalnumber="1799" number="37" form="verse">What e&#8217;er falls more. We must to horse again.</line>
<line globalnumber="1800" number="38" form="verse">Go, go, provide.</line>
</speech>

<stagedir sdglobalnumber="1800.01" sdnumber="38.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>HEL.</actor>
		<actor>WID.</actor>
		<actor>DIA.</actor>
		<actor>GENT.</actor>
		<actor>Attendants</actor>
	</action>
</stagedir>

</scene>

<scene actnum="5" num="2">
<scenetitle>Scene 2</scenetitle>
<scenelocation>Roussillon. Before the Count&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="CLO.">Clown Lavatch</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
	<scenepersona short="LAF.">Lafew</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1800.02" sdnumber="0.01">
	<dir>Enter Clown Lavatch and Parolles.</dir>
	<action type="enter">
		<actor>CLO.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1801" number="1" form="prose">Good Master Lavatch, give my Lord Lafew this letter. I have ere now, sir, been better known to you, when I have held familiarity with fresher clothes; but I am now, sir, muddied in Fortune&#8217;s mood, and smell somewhat strong of her strong displeasure.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1802" number="2" form="prose">Truly, Fortune&#8217;s displeasure is but sluttish if it smell so strongly as thou speak&#8217;st of. I will henceforth eat no fish of Fortune&#8217;s butt&#8217;ring. Prithee allow the wind.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1803" number="3" form="prose">Nay, you need not to stop your nose, sir; I spake but by a metaphor.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1804" number="4" form="prose">Indeed, sir, if your metaphor stink, I will stop my nose, or against any man&#8217;s metaphor. Prithee get thee further.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1805" number="5" form="prose">Pray you, sir, deliver me this paper.</line>
</speech>

<speech>
<speaker long="Lavatch">CLO.</speaker>
<line globalnumber="1806" number="6" form="prose">Foh, prithee stand away. A paper from Fortune&#8217;s close-stool to give to a nobleman! Look here he comes himself.</line>
<stagedir sdglobalnumber="1806.01" sdnumber="6.01">
	<dir>Enter Lafew.</dir>
	<action type="enter">
		<actor>LAF.</actor>
	</action>
</stagedir>
<line globalnumber="1807" number="7" form="prose">Here is a purr of Fortune&#8217;s, sir, or of Fortune&#8217;s cat&#8212;but not a musk-cat&#8212;that has fall&#8217;n into the unclean fishpond of her displeasure, and as he says, is muddied withal. Pray you, sir, use the carp as you may, for he looks like a poor, decay&#8217;d, ingenious, foolish, rascally knave. I do pity his distress in my similes of comfort, and leave him to your lordship.</line>
</speech>

<stagedir sdglobalnumber="1807.01" sdnumber="7.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>CLO.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1808" number="8" form="prose">My lord, I am a man whom Fortune hath cruelly scratch&#8217;d.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1809" number="9" form="prose">And what would you have me to do? &#8217;Tis too late to pare her nails now. Wherein have you play&#8217;d the knave with Fortune that she should scratch you, who of herself is a good lady, and would not have knaves thrive long under her? There&#8217;s a cardecue for you. Let the justices make you and Fortune friends; I am for other business.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1810" number="10" form="prose">I beseech your honor to hear me one single word.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1811" number="11" form="prose">You beg a single penny more. Come, you shall ha&#8217;t; save your word.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1812" number="12" form="prose">My name, my good lord, is Parolles.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1813" number="13" form="prose">You beg more than &#8220;word&#8221; then. Cox my passion! Give me your hand. How does your drum?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1814" number="14" form="prose">O my good lord, you were the first that found me!</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1815" number="15" form="prose">Was I, in sooth? And I was the first that lost thee.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1816" number="16" form="prose">It lies in you, my lord, to bring me in some grace, for you did bring me out.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1817" number="17" form="prose">Out upon thee, knave! Dost thou put upon me at once both the office of God and the devil? One brings thee in grace, and the other brings thee out.</line>
<stagedir sdglobalnumber="1817.01" sdnumber="17.01">
	<dir>Trumpets sound.</dir>
	<action type="sound">
	</action>
</stagedir>
<line globalnumber="1818" number="18" form="prose">The King&#8217;s coming, I know by his trumpets. Sirrah, inquire further after me. I had talk of you last night; though you are a fool and a knave, you shall eat. Go to, follow.</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="1819" number="19" form="prose">I praise God for you.</line>
</speech>

<stagedir sdglobalnumber="1819.01" sdnumber="19.01">
	<dir>Exeunt.</dir>
	<action type="exit">
		<actor>LAF.</actor>
		<actor>PAR.</actor>
	</action>
</stagedir>

</scene>

<scene actnum="5" num="3">
<scenetitle>Scene 3</scenetitle>
<scenelocation>Roussillon. The Count&#8217;s palace.</scenelocation>

<scenepersonae>
	<scenepersona short="KING.">King</scenepersona>
	<scenepersona short="COUNT.">Countess of Roussillon</scenepersona>
	<scenepersona short="LAF.">Lafew</scenepersona>
	<scenepersona short="BOTH LORDS.">two French Lords</scenepersona>
	<scenepersona>Attendant</scenepersona>
	<scenepersona short="BER.">Bertram</scenepersona>
	<scenepersona short="GENT.">Gentleman</scenepersona>
	<scenepersona short="WID.">Old Widow of Florence</scenepersona>
	<scenepersona short="DIA.">Diana</scenepersona>
	<scenepersona short="PAR.">Parolles</scenepersona>
	<scenepersona short="HEL.">Helena</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<stagedir sdglobalnumber="1819.02" sdnumber="0.01">
	<dir>Flourish. Enter King, old Lady Countess, Lafew, the two French Lords, with Attendants.</dir>
	<action type="enter">
		<actor>KING.</actor>
		<actor>COUNT.</actor>
		<actor>LAF.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
		<actor>GENT.</actor>
		<actor>Attendants</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1820" number="1" form="verse">We lost a jewel of her, and our esteem</line>
<line globalnumber="1821" number="2" form="verse">Was made much poorer by it; but your son,</line>
<line globalnumber="1822" number="3" form="verse">As mad in folly, lack&#8217;d the sense to know</line>
<line globalnumber="1823" number="4" form="verse" offset="0">Her estimation home.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1824" number="4" form="verse" offset="5">&#8217;Tis past, my liege,</line>
<line globalnumber="1825" number="5" form="verse">And I beseech your Majesty to make it</line>
<line globalnumber="1826" number="6" form="verse">Natural rebellion, done i&#8217; th&#8217; blade of youth,</line>
<line globalnumber="1827" number="7" form="verse">When oil and fire, too strong for reason&#8217;s force,</line>
<line globalnumber="1828" number="8" form="verse" offset="0">O&#8217;erbears it, and burns on.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1829" number="8" form="verse" offset="6">My honor&#8217;d lady,</line>
<line globalnumber="1830" number="9" form="verse">I have forgiven and forgotten all,</line>
<line globalnumber="1831" number="10" form="verse">Though my revenges were high bent upon him,</line>
<line globalnumber="1832" number="11" form="verse" offset="0">And watch&#8217;d the time to shoot.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1833" number="11" form="verse" offset="7">This I must say&#8212;</line>
<line globalnumber="1834" number="12" form="verse">But first I beg my pardon&#8212;the young lord</line>
<line globalnumber="1835" number="13" form="verse">Did to his Majesty, his mother, and his lady</line>
<line globalnumber="1836" number="14" form="verse">Offense of mighty note; but to himself</line>
<line globalnumber="1837" number="15" form="verse">The greatest wrong of all. He lost a wife</line>
<line globalnumber="1838" number="16" form="verse">Whose beauty did astonish the survey</line>
<line globalnumber="1839" number="17" form="verse">Of richest eyes, whose words all ears took captive,</line>
<line globalnumber="1840" number="18" form="verse">Whose dear perfection hearts that scorn&#8217;d to serve</line>
<line globalnumber="1841" number="19" form="verse" offset="0">Humbly call&#8217;d mistress.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1842" number="19" form="verse" offset="5">Praising what is lost</line>
<line globalnumber="1843" number="20" form="verse">Makes the remembrance dear. Well, call him hither,</line>
<line globalnumber="1844" number="21" form="verse">We are reconcil&#8217;d, and the first view shall kill</line>
<line globalnumber="1845" number="22" form="verse">All repetition. Let him not ask our pardon,</line>
<line globalnumber="1846" number="23" form="verse">The nature of his great offense is dead,</line>
<line globalnumber="1847" number="24" form="verse">And deeper than oblivion we do bury</line>
<line globalnumber="1848" number="25" form="verse">Th&#8217; incensing relics of it. Let him approach</line>
<line globalnumber="1849" number="26" form="verse">A stranger, no offender; and inform him</line>
<line globalnumber="1850" number="27" form="verse" offset="0">So &#8217;tis our will he should.</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1851" number="27" form="verse" offset="5">I shall, my liege.</line>
</speech>

<stagedir sdglobalnumber="1851.01" sdnumber="27.01">
	<dir>Exit.</dir>
	<action type="exit">
		<actor>GENT.</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1852" number="28" form="verse">What says he to your daughter? Have you spoke?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1853" number="29" form="verse">All that he is hath reference to your Highness.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1854" number="30" form="verse">Then shall we have a match. I have letters sent me</line>
<line globalnumber="1855" number="31" form="verse" offset="0">That sets him high in fame.</line>
</speech>

<stagedir sdglobalnumber="1855.01" sdnumber="31.01">
	<dir>Enter Count Bertram.</dir>
	<action type="enter">
		<actor>BER.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1856" number="31" form="verse" offset="6">He looks well on&#8217;t.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1857" number="32" form="verse">I am not a day of season,</line>
<line globalnumber="1858" number="33" form="verse">For thou mayst see a sunshine and a hail</line>
<line globalnumber="1859" number="34" form="verse">In me at once. But to the brightest beams</line>
<line globalnumber="1860" number="35" form="verse">Distracted clouds give way, so stand thou forth,</line>
<line globalnumber="1861" number="36" form="verse" offset="0">The time is fair again.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1862" number="36" form="verse" offset="4">My high-repented blames,</line>
<line globalnumber="1863" number="37" form="verse" offset="0">Dear sovereign, pardon to me.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1864" number="37" form="verse" offset="7">All is whole,</line>
<line globalnumber="1865" number="38" form="verse">Not one word more of the consumed time.</line>
<line globalnumber="1866" number="39" form="verse">Let&#8217;s take the instant by the forward top;</line>
<line globalnumber="1867" number="40" form="verse">For we are old, and on our quick&#8217;st decrees</line>
<line globalnumber="1868" number="41" form="verse">Th&#8217; inaudible and noiseless foot of time</line>
<line globalnumber="1869" number="42" form="verse">Steals ere we can effect them. You remember</line>
<line globalnumber="1870" number="43" form="verse">The daughter of this lord?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1871" number="44" form="verse">Admiringly, my liege. At first</line>
<line globalnumber="1872" number="45" form="verse">I stuck my choice upon her, ere my heart</line>
<line globalnumber="1873" number="46" form="verse">Durst make too bold a herald of my tongue;</line>
<line globalnumber="1874" number="47" form="verse">Where the impression of mine eye infixing,</line>
<line globalnumber="1875" number="48" form="verse">Contempt his scornful perspective did lend me,</line>
<line globalnumber="1876" number="49" form="verse">Which warp&#8217;d the line of every other favor,</line>
<line globalnumber="1877" number="50" form="verse">Scorn&#8217;d a fair color, or express&#8217;d it stol&#8217;n,</line>
<line globalnumber="1878" number="51" form="verse">Extended or contracted all proportions</line>
<line globalnumber="1879" number="52" form="verse">To a most hideous object. Thence it came</line>
<line globalnumber="1880" number="53" form="verse">That she whom all men prais&#8217;d, and whom myself,</line>
<line globalnumber="1881" number="54" form="verse">Since I have lost, have lov&#8217;d, was in mine eye</line>
<line globalnumber="1882" number="55" form="verse" offset="0">The dust that did offend it.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1883" number="55" form="verse" offset="7">Well excus&#8217;d.</line>
<line globalnumber="1884" number="56" form="verse">That thou didst love her, strikes some scores away</line>
<line globalnumber="1885" number="57" form="verse">From the great compt; but love that comes too late,</line>
<line globalnumber="1886" number="58" form="verse">Like a remorseful pardon slowly carried,</line>
<line globalnumber="1887" number="59" form="verse">To the great sender turns a sour offense,</line>
<line globalnumber="1888" number="60" form="verse">Crying, &#8220;That&#8217;s good that&#8217;s gone.&#8221; Our rash faults</line>
<line globalnumber="1889" number="61" form="verse">Make trivial price of serious things we have,</line>
<line globalnumber="1890" number="62" form="verse">Not knowing them until we know their grave.</line>
<line globalnumber="1891" number="63" form="verse">Oft our displeasures, to ourselves unjust,</line>
<line globalnumber="1892" number="64" form="verse">Destroy our friends, and after weep their dust;</line>
<line globalnumber="1893" number="65" form="verse">Our own love waking cries to see what&#8217;s done,</line>
<line globalnumber="1894" number="66" form="verse">While shameful hate sleeps out the afternoon.</line>
<line globalnumber="1895" number="67" form="verse">Be this sweet Helen&#8217;s knell, and now forget her.</line>
<line globalnumber="1896" number="68" form="verse">Send forth your amorous token for fair Maudlin.</line>
<line globalnumber="1897" number="69" form="verse">The main consents are had, and here we&#8217;ll stay</line>
<line globalnumber="1898" number="70" form="verse">To see our widower&#8217;s second marriage-day.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1899" number="71" form="verse">Which better than the first, O dear heaven, bless!</line>
<line globalnumber="1900" number="72" form="verse">Or, ere they meet, in me, O nature, cesse!</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1901" number="73" form="verse">Come on, my son, in whom my house&#8217;s name</line>
<line globalnumber="1902" number="74" form="verse">Must be digested; give a favor from you</line>
<line globalnumber="1903" number="75" form="verse">To sparkle in the spirits of my daughter,</line>
<line globalnumber="1904" number="76" form="verse" offset="0">That she may quickly come.</line>
<stagedir sdglobalnumber="1904.01" sdnumber="76.01">
	<dir>Bertram gives a ring.</dir>
	<action type="action">
		<actor>BER.</actor>
		<recipient>LAF.</recipient>
	</action>
</stagedir>
<line globalnumber="1905" number="76" form="verse" offset="5">By my old beard,</line>
<line globalnumber="1906" number="77" form="verse">And ev&#8217;ry hair that&#8217;s on&#8217;t, Helen, that&#8217;s dead,</line>
<line globalnumber="1907" number="78" form="verse">Was a sweet creature; such a ring as this,</line>
<line globalnumber="1908" number="79" form="verse">The last that e&#8217;er I took her leave at court,</line>
<line globalnumber="1909" number="80" form="verse" offset="0">I saw upon her finger.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1910" number="80" form="verse" offset="5">Hers it was not.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1911" number="81" form="verse">Now pray you let me see it; for mine eye,</line>
<line globalnumber="1912" number="82" form="verse">While I was speaking, oft was fasten&#8217;d to&#8217;t.</line>
<line globalnumber="1913" number="83" form="verse">This ring was mine, and when I gave it Helen,</line>
<line globalnumber="1914" number="84" form="verse">I bade her, if her fortunes ever stood</line>
<line globalnumber="1915" number="85" form="verse">Necessitied to help, that by this token</line>
<line globalnumber="1916" number="86" form="verse">I would relieve her. Had you that craft to reave her</line>
<line globalnumber="1917" number="87" form="verse" offset="0">Of what should stead her most?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1918" number="87" form="verse" offset="6">My gracious sovereign,</line>
<line globalnumber="1919" number="88" form="verse">Howe&#8217;er it pleases you to take it so,</line>
<line globalnumber="1920" number="89" form="verse" offset="0">The ring was never hers.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1921" number="89" form="verse" offset="5">Son, on my life,</line>
<line globalnumber="1922" number="90" form="verse">I have seen her wear it, and she reckon&#8217;d it</line>
<line globalnumber="1923" number="91" form="verse" offset="0">At her live&#8217;s rate.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1924" number="91" form="verse" offset="4">I am sure I saw her wear it.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1925" number="92" form="verse">You are deceiv&#8217;d, my lord, she never saw it.</line>
<line globalnumber="1926" number="93" form="verse">In Florence was it from a casement thrown me,</line>
<line globalnumber="1927" number="94" form="verse">Wrapp&#8217;d in a paper, which contain&#8217;d the name</line>
<line globalnumber="1928" number="95" form="verse">Of her that threw it. Noble she was, and thought</line>
<line globalnumber="1929" number="96" form="verse">I stood engag&#8217;d; but when I had subscrib&#8217;d</line>
<line globalnumber="1930" number="97" form="verse">To mine own fortune, and inform&#8217;d her fully</line>
<line globalnumber="1931" number="98" form="verse">I could not answer in that course of honor</line>
<line globalnumber="1932" number="99" form="verse">As she had made the overture, she ceas&#8217;d</line>
<line globalnumber="1933" number="100" form="verse">In heavy satisfaction, and would never</line>
<line globalnumber="1934" number="101" form="verse" offset="0">Receive the ring again.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1935" number="101" form="verse" offset="5">Plutus himself,</line>
<line globalnumber="1936" number="102" form="verse">That knows the tinct and multiplying med&#8217;cine,</line>
<line globalnumber="1937" number="103" form="verse">Hath not in nature&#8217;s mystery more science</line>
<line globalnumber="1938" number="104" form="verse">Than I have in this ring. &#8217;Twas mine, &#8217;twas Helen&#8217;s,</line>
<line globalnumber="1939" number="105" form="verse">Whoever gave it you. Then if you know</line>
<line globalnumber="1940" number="106" form="verse">That you are well acquainted with yourself,</line>
<line globalnumber="1941" number="107" form="verse">Confess &#8217;twas hers, and by what rough enforcement</line>
<line globalnumber="1942" number="108" form="verse">You got it from her. She call&#8217;d the saints to surety</line>
<line globalnumber="1943" number="109" form="verse">That she would never put it from her finger,</line>
<line globalnumber="1944" number="110" form="verse">Unless she gave it to yourself in bed,</line>
<line globalnumber="1945" number="111" form="verse">Where you have never come, or sent it us</line>
<line globalnumber="1946" number="112" form="verse" offset="0">Upon her great disaster.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1947" number="112" form="verse" offset="5">She never saw it.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1948" number="113" form="verse">Thou speak&#8217;st it falsely, as I love mine honor,</line>
<line globalnumber="1949" number="114" form="verse">And mak&#8217;st conjectural fears to come into me,</line>
<line globalnumber="1950" number="115" form="verse">Which I would fain shut out. If it should prove</line>
<line globalnumber="1951" number="116" form="verse">That thou art so inhuman&#8212;&#8217;twill not prove so;</line>
<line globalnumber="1952" number="117" form="verse">And yet I know not: thou didst hate her deadly,</line>
<line globalnumber="1953" number="118" form="verse">And she is dead, which nothing but to close</line>
<line globalnumber="1954" number="119" form="verse">Her eyes myself could win me to believe,</line>
<line globalnumber="1955" number="120" form="verse">More than to see this ring. Take him away.</line>
<stagedir sdglobalnumber="1955.01" sdnumber="120.01">
	<dir>Guards seize Bertram.</dir>
	<action type="action">
		<recipient>BER.</recipient>
	</action>
</stagedir>
<line globalnumber="1956" number="121" form="verse">My fore-past proofs, howe&#8217;er the matter fall,</line>
<line globalnumber="1957" number="122" form="verse">Shall tax my fears of little vanity,</line>
<line globalnumber="1958" number="123" form="verse">Having vainly fear&#8217;d too little. Away with him!</line>
<line globalnumber="1959" number="124" form="verse" offset="0">We&#8217;ll sift this matter further.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1960" number="124" form="verse" offset="6">If you shall prove</line>
<line globalnumber="1961" number="125" form="verse">This ring was ever hers, you shall as easy</line>
<line globalnumber="1962" number="126" form="verse">Prove that I husbanded her bed in Florence,</line>
<line globalnumber="1963" number="127" form="verse">Where yet she never was.</line>
</speech>

<stagedir sdglobalnumber="1963.01" sdnumber="127.01">
	<dir>Exit guarded.</dir>
	<action type="exit">
		<actor>BER.</actor>
	</action>
</stagedir>

<stagedir sdglobalnumber="1963.02" sdnumber="127.02">
	<dir>Enter a Gentleman, the astringer.</dir>
	<action type="enter">
		<actor>GENT.</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1964" number="128" form="verse" offset="0">I am wrapp&#8217;d in dismal thinkings.</line>
</speech>

<speech>
<speaker long="Gentleman">GENT.</speaker>
<line globalnumber="1965" number="128" form="verse" offset="7">Gracious sovereign,</line>
<line globalnumber="1966" number="129" form="verse">Whether I have been to blame or no, I know not.</line>
<line globalnumber="1967" number="130" form="verse">Here&#8217;s a petition from a Florentine,</line>
<line globalnumber="1968" number="131" form="verse">Who hath for four or five removes come short</line>
<line globalnumber="1969" number="132" form="verse">To tender it herself. I undertook it,</line>
<line globalnumber="1970" number="133" form="verse">Vanquish&#8217;d thereto by the fair grace and speech</line>
<line globalnumber="1971" number="134" form="verse">Of the poor suppliant, who by this I know</line>
<line globalnumber="1972" number="135" form="verse">Is here attending. Her business looks in her</line>
<line globalnumber="1973" number="136" form="verse">With an importing visage, and she told me,</line>
<line globalnumber="1974" number="137" form="verse">In a sweet verbal brief, it did concern</line>
<line globalnumber="1975" number="138" form="verse">Your Highness with herself.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<stagedir sdglobalnumber="1975.01" sdnumber="138.01">
	<dir>Reads a letter.</dir>
	<action type="read">
		<actor>KING.</actor>
	</action>
</stagedir>
<line globalnumber="1976" number="139" form="prose"><recite>&#8220;Upon his many protestations to marry me when his wife was dead, I blush to say it, he won me. Now is the Count Roussillon a widower, his vows are forfeited to me, and my honor&#8217;s paid to him. He stole from Florence, taking no leave, and I follow him to his country for justice. Grant it me, O King, in you it best lies; otherwise a seducer flourishes, and a poor maid is undone. Diana Capilet.&#8221;</recite></line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="1977" number="140" form="prose">I will buy me a son-in-law in a fair, and toll for this. I&#8217;ll none of him.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1978" number="141" form="verse">The heavens have thought well on thee, Lafew,</line>
<line globalnumber="1979" number="142" form="verse">To bring forth this discov&#8217;ry. Seek these suitors.</line>
<line globalnumber="1980" number="143" form="verse">Go speedily, and bring again the Count.</line>
<stagedir sdglobalnumber="1980.01" sdnumber="143.01">
	<dir>Exeunt some Attendants.</dir>
	<action type="exit">
	</action>
</stagedir>
<line globalnumber="1981" number="144" form="verse">I am afeard the life of Helen, lady,</line>
<line globalnumber="1982" number="145" form="verse" offset="0">Was foully snatch&#8217;d.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="1983" number="145" form="verse" offset="4">Now, justice on the doers!</line>
</speech>

<stagedir sdglobalnumber="1983.01" sdnumber="145.01">
	<dir>Enter Bertram guarded.</dir>
	<action type="enter">
		<actor>BER.</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1984" number="146" form="verse">I wonder, sir, sith wives are monsters to you,</line>
<line globalnumber="1985" number="147" form="verse">And that you fly them as you swear them lordship,</line>
<line globalnumber="1986" number="148" form="verse">Yet you desire to marry. What woman&#8217;s that?</line>
</speech>

<stagedir sdglobalnumber="1986.01" sdnumber="148.01">
	<dir>Enter Widow, Diana.</dir>
	<action type="enter">
		<actor>DIA.</actor>
		<actor>WID.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1987" number="149" form="verse">I am, my lord, a wretched Florentine,</line>
<line globalnumber="1988" number="150" form="verse">Derived from the ancient Capilet.</line>
<line globalnumber="1989" number="151" form="verse">My suit, as I do understand, you know,</line>
<line globalnumber="1990" number="152" form="verse">And therefore know how far I may be pitied.</line>
</speech>

<speech>
<speaker long="An Old Widow of Florence">WID.</speaker>
<line globalnumber="1991" number="153" form="verse">I am her mother, sir, whose age and honor</line>
<line globalnumber="1992" number="154" form="verse">Both suffer under this complaint we bring,</line>
<line globalnumber="1993" number="155" form="verse">And both shall cease, without your remedy.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="1994" number="156" form="verse">Come hither, Count, do you know these women?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1995" number="157" form="verse">My lord, I neither can nor will deny</line>
<line globalnumber="1996" number="158" form="verse">But that I know them. Do they charge me further?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1997" number="159" form="verse">Why do you look so strange upon your wife?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="1998" number="160" form="verse" offset="0">She&#8217;s none of mine, my lord.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="1999" number="160" form="verse" offset="6">If you shall marry,</line>
<line globalnumber="2000" number="161" form="verse">You give away this hand, and that is mine;</line>
<line globalnumber="2001" number="162" form="verse">You give away heaven&#8217;s vows, and those are mine;</line>
<line globalnumber="2002" number="163" form="verse">You give away myself, which is known mine;</line>
<line globalnumber="2003" number="164" form="verse">For I by vow am so embodied yours,</line>
<line globalnumber="2004" number="165" form="verse">That she which marries you must marry me,</line>
<line globalnumber="2005" number="166" form="verse">Either both or none.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="2006" number="167" form="prose">Your reputation comes too short for my daughter, you are no husband for her.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2007" number="168" form="verse">My lord, this is a fond and desp&#8217;rate creature,</line>
<line globalnumber="2008" number="169" form="verse">Whom sometime I have laugh&#8217;d with. Let your Highness</line>
<line globalnumber="2009" number="170" form="verse">Lay a more noble thought upon mine honor</line>
<line globalnumber="2010" number="171" form="verse">Than for to think that I would sink it here.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2011" number="172" form="verse">Sir, for my thoughts, you have them ill to friend</line>
<line globalnumber="2012" number="173" form="verse">Till your deeds gain them; fairer prove your honor</line>
<line globalnumber="2013" number="174" form="verse" offset="0">Than in my thought it lies.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2014" number="174" form="verse" offset="5">Good my lord,</line>
<line globalnumber="2015" number="175" form="verse">Ask him upon his oath, if he does think</line>
<line globalnumber="2016" number="176" form="verse">He had not my virginity.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2017" number="177" form="verse" offset="0">What say&#8217;st thou to her?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2018" number="177" form="verse" offset="5">She&#8217;s impudent, my lord,</line>
<line globalnumber="2019" number="178" form="verse">And was a common gamester to the camp.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2020" number="179" form="verse">He does me wrong, my lord; if I were so,</line>
<line globalnumber="2021" number="180" form="verse">He might have bought me at a common price.</line>
<line globalnumber="2022" number="181" form="verse">Do not believe him. O, behold this ring,</line>
<line globalnumber="2023" number="182" form="verse">Whose high respect and rich validity</line>
<line globalnumber="2024" number="183" form="verse">Did lack a parallel; yet for all that</line>
<line globalnumber="2025" number="184" form="verse">He gave it to a commoner a&#8217; th&#8217; camp,</line>
<line globalnumber="2026" number="185" form="verse" offset="0">If I be one.</line>
</speech>

<speech>
<speaker long="Countess of Roussillon">COUNT.</speaker>
<line globalnumber="2027" number="185" form="verse" offset="3">He blushes, and &#8217;tis hit.</line>
<line globalnumber="2028" number="186" form="verse">Of six preceding ancestors, that gem,</line>
<line globalnumber="2029" number="187" form="verse">Conferr&#8217;d by testament to th&#8217; sequent issue,</line>
<line globalnumber="2030" number="188" form="verse">Hath it been owed and worn. This is his wife,</line>
<line globalnumber="2031" number="189" form="verse" offset="0">That ring&#8217;s a thousand proofs.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2032" number="189" form="verse" offset="6">Methought you said</line>
<line globalnumber="2033" number="190" form="verse">You saw one here in court could witness it.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2034" number="191" form="verse">I did, my lord, but loath am to produce</line>
<line globalnumber="2035" number="192" form="verse">So bad an instrument. His name&#8217;s Parolles.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="2036" number="193" form="verse">I saw the man today, if man he be.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2037" number="194" form="verse" offset="0">Find him, and bring him hither.</line>
</speech>

<stagedir sdglobalnumber="2037.01" sdnumber="194.01">
	<dir>Exit an Attendant.</dir>
	<action type="exit">
	</action>
</stagedir>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2038" number="194" form="verse" offset="7">What of him?</line>
<line globalnumber="2039" number="195" form="verse">He&#8217;s quoted for a most perfidious slave,</line>
<line globalnumber="2040" number="196" form="verse">With all the spots a&#8217; th&#8217; world tax&#8217;d and debosh&#8217;d,</line>
<line globalnumber="2041" number="197" form="verse">Whose nature sickens but to speak a truth.</line>
<line globalnumber="2042" number="198" form="verse">Am I or that or this for what he&#8217;ll utter,</line>
<line globalnumber="2043" number="199" form="verse" offset="0">That will speak any thing?</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2044" number="199" form="verse" offset="5">She hath that ring of yours.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2045" number="200" form="verse">I think she has. Certain it is I lik&#8217;d her,</line>
<line globalnumber="2046" number="201" form="verse">And boarded her i&#8217; th&#8217; wanton way of youth.</line>
<line globalnumber="2047" number="202" form="verse">She knew her distance, and did angle for me,</line>
<line globalnumber="2048" number="203" form="verse">Madding my eagerness with her restraint,</line>
<line globalnumber="2049" number="204" form="verse">As all impediments in fancy&#8217;s course</line>
<line globalnumber="2050" number="205" form="verse">Are motives of more fancy, and in fine,</line>
<line globalnumber="2051" number="206" form="verse">Her inf&#8217;nite cunning, with her modern grace,</line>
<line globalnumber="2052" number="207" form="verse">Subdu&#8217;d me to her rate. She got the ring,</line>
<line globalnumber="2053" number="208" form="verse">And I had that which any inferior might</line>
<line globalnumber="2054" number="209" form="verse" offset="0">At market-price have bought.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2055" number="209" form="verse" offset="6">I must be patient.</line>
<line globalnumber="2056" number="210" form="verse">You that have turn&#8217;d off a first so noble wife,</line>
<line globalnumber="2057" number="211" form="verse">May justly diet me. I pray you yet</line>
<line globalnumber="2058" number="212" form="verse">(Since you lack virtue, I will lose a husband)</line>
<line globalnumber="2059" number="213" form="verse">Send for your ring, I will return it home,</line>
<line globalnumber="2060" number="214" form="verse" offset="0">And give me mine again.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2061" number="214" form="verse" offset="5">I have it not.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2062" number="215" form="verse" offset="0">What ring was yours, I pray you?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2063" number="215" form="verse" offset="7">Sir, much like</line>
<line globalnumber="2064" number="216" form="verse">The same upon your finger.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2065" number="217" form="verse">Know you this ring? This ring was his of late.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2066" number="218" form="verse">And this was it I gave him, being a-bed.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2067" number="219" form="verse">The story then goes false, you threw it him</line>
<line globalnumber="2068" number="220" form="verse" offset="0">Out of a casement.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2069" number="220" form="verse" offset="4">I have spoke the truth.</line>
</speech>

<stagedir sdglobalnumber="2069.01" sdnumber="220.01">
	<dir>Enter Parolles.</dir>
	<action type="enter">
		<actor>PAR.</actor>
	</action>
</stagedir>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2070" number="221" form="verse">My lord, I do confess the ring was hers.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2071" number="222" form="verse">You boggle shrewdly, every feather starts you.</line>
<line globalnumber="2072" number="223" form="verse" offset="0">Is this the man you speak of?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2073" number="223" form="verse" offset="6">Ay, my lord.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2074" number="224" form="verse">Tell me, sirrah&#8212;but tell me true, I charge you,</line>
<line globalnumber="2075" number="225" form="verse">Not fearing the displeasure of your master,</line>
<line globalnumber="2076" number="226" form="verse">Which on your just proceeding I&#8217;ll keep off&#8212;</line>
<line globalnumber="2077" number="227" form="verse">By him and by this woman here what know you?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="2078" number="228" form="prose">So please your Majesty, my master hath been an honorable gentleman. Tricks he hath had in him, which gentlemen have.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2079" number="229" form="prose">Come, come, to th&#8217; purpose. Did he love this woman?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="2080" number="230" form="prose">Faith, sir, he did love her, but how?</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2081" number="231" form="prose">How, I pray you?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="2082" number="232" form="prose">He did love her, sir, as a gentleman loves a woman.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2083" number="233" form="prose">How is that?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="2084" number="234" form="prose">He lov&#8217;d her, sir, and lov&#8217;d her not.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2085" number="235" form="prose">As thou art a knave, and no knave. What an equivocal companion is this!</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="2086" number="236" form="prose">I am a poor man, and at your Majesty&#8217;s command.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="2087" number="237" form="prose">He&#8217;s a good drum, my lord, but a naughty orator.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2088" number="238" form="prose">Do you know he promis&#8217;d me marriage?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="2089" number="239" form="prose">Faith, I know more than I&#8217;ll speak.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2090" number="240" form="prose">But wilt thou not speak all thou know&#8217;st?</line>
</speech>

<speech>
<speaker long="Parolles">PAR.</speaker>
<line globalnumber="2091" number="241" form="prose">Yes, so please your Majesty. I did go between them as I said, but more than that, he lov&#8217;d her, for indeed he was mad for her, and talk&#8217;d of Satan and of Limbo and of Furies and I know not what. Yet I was in that credit with them at that time that I knew of their going to bed, and of other motions, as promising her marriage, and things which would derive me ill will to speak of; therefore I will not speak what I know.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2092" number="242" form="prose">Thou hast spoken all already, unless thou canst say they are married. But thou art too fine in thy evidence, therefore stand aside.</line>
<line globalnumber="2093" number="243" form="verse" offset="0">This ring you say was yours?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2094" number="243" form="verse" offset="6">Ay, my good lord.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2095" number="244" form="verse">Where did you buy it? Or who gave it you?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2096" number="245" form="verse">It was not given me, nor I did not buy it.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2097" number="246" form="verse" offset="0">Who lent it you?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2098" number="246" form="verse" offset="4">It was not lent me neither.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2099" number="247" form="verse" offset="0">Where did you find it then?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2100" number="247" form="verse" offset="5">I found it not.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2101" number="248" form="verse">If it were yours by none of all these ways,</line>
<line globalnumber="2102" number="249" form="verse" offset="0">How could you give it him?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2103" number="249" form="verse" offset="5">I never gave it him.</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="2104" number="250" form="prose">This woman&#8217;s an easy glove, my lord, she goes off and on at pleasure.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2105" number="251" form="verse">This ring was mine, I gave it his first wife.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2106" number="252" form="verse">It might be yours or hers for aught I know.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2107" number="253" form="verse">Take her away, I do not like her now,</line>
<line globalnumber="2108" number="254" form="verse">To prison with her; and away with him.</line>
<line globalnumber="2109" number="255" form="verse">Unless thou tell&#8217;st me where thou hadst this ring,</line>
<line globalnumber="2110" number="256" form="verse" offset="0">Thou diest within this hour.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2111" number="256" form="verse" offset="5">I&#8217;ll never tell you.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2112" number="257" form="verse" offset="0">Take her away.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2113" number="257" form="verse" offset="3">I&#8217;ll put in bail, my liege.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2114" number="258" form="verse">I think thee now some common customer.</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2115" number="259" form="verse">By Jove, if ever I knew man, &#8217;twas you.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2116" number="260" form="verse">Wherefore hast thou accus&#8217;d him all this while?</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2117" number="261" form="verse">Because he&#8217;s guilty, and he is not guilty.</line>
<line globalnumber="2118" number="262" form="verse">He knows I am no maid, and he&#8217;ll swear to&#8217;t;</line>
<line globalnumber="2119" number="263" form="verse">I&#8217;ll swear I am a maid, and he knows not.</line>
<line globalnumber="2120" number="264" form="verse">Great King, I am no strumpet, by my life;</line>
<line globalnumber="2121" number="265" form="verse">I am either maid, or else this old man&#8217;s wife.</line>
</speech>

<stagedir sdglobalnumber="2121.01" sdnumber="265.01">
	<dir>Pointing to Lafew.</dir>
	<action type="action">
		<actor>DIA.</actor>
		<recipient>LAF.</recipient>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2122" number="266" form="verse">She does abuse our ears. To prison with her!</line>
</speech>

<speech>
<speaker long="Diana">DIA.</speaker>
<line globalnumber="2123" number="267" form="verse">Good mother, fetch my bail.</line>
<stagedir sdglobalnumber="2123.01" sdnumber="267.01">
	<dir>Exit Widow.</dir>
	<action type="exit">
		<actor>WID.</actor>
	</action>
</stagedir>
<line globalnumber="2124" number="268" form="verse">Stay, royal sir.</line>
<line globalnumber="2125" number="269" form="verse">The jeweler that owes the ring is sent for,</line>
<line globalnumber="2126" number="270" form="verse">And he shall surety me. But for this lord,</line>
<line globalnumber="2127" number="271" form="verse">Who hath abus&#8217;d me, as he knows himself,</line>
<line globalnumber="2128" number="272" form="verse">Though yet he never harm&#8217;d me, here I quit him.</line>
<line globalnumber="2129" number="273" form="verse">He knows himself my bed he hath defil&#8217;d,</line>
<line globalnumber="2130" number="274" form="verse">And at that time he got his wife with child.</line>
<line globalnumber="2131" number="275" form="verse">Dead though she be, she feels her young one kick.</line>
<line globalnumber="2132" number="276" form="verse">So there&#8217;s my riddle: one that&#8217;s dead is quick&#8212;</line>
<line globalnumber="2133" number="277" form="verse" offset="0">And now behold the meaning.</line>
</speech>

<stagedir sdglobalnumber="2133.01" sdnumber="277.01">
	<dir>Enter Widow and Helen.</dir>
	<action type="enter">
		<actor>WID.</actor>
		<actor>HEL.</actor>
	</action>
</stagedir>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2134" number="277" form="verse" offset="6">Is there no exorcist</line>
<line globalnumber="2135" number="278" form="verse">Beguiles the truer office of mine eyes?</line>
<line globalnumber="2136" number="279" form="verse" offset="0">Is&#8217;t real that I see?</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="2137" number="279" form="verse" offset="4">No, my good lord,</line>
<line globalnumber="2138" number="280" form="verse">&#8217;Tis but the shadow of a wife you see,</line>
<line globalnumber="2139" number="281" form="verse" offset="0">The name, and not the thing.</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2140" number="281" form="verse" offset="6">Both, both. O, pardon!</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="2141" number="282" form="verse">O my good lord, when I was like this maid,</line>
<line globalnumber="2142" number="283" form="verse">I found you wondrous kind. There is your ring,</line>
<line globalnumber="2143" number="284" form="verse">And look you, here&#8217;s your letter. This it says:</line>
<line globalnumber="2144" number="285" form="verse">&#8220;When from my finger you can get this ring,</line>
<line globalnumber="2145" number="286" form="verse">And are by me with child, etc.&#8221; This is done.</line>
<line globalnumber="2146" number="287" form="verse">Will you be mine now you are doubly won?</line>
</speech>

<speech>
<speaker long="Bertram, Count of Roussillon">BER.</speaker>
<line globalnumber="2147" number="288" form="verse">If she, my liege, can make me know this clearly,</line>
<line globalnumber="2148" number="289" form="verse">I&#8217;ll love her dearly, ever, ever dearly.</line>
</speech>

<speech>
<speaker long="Helena">HEL.</speaker>
<line globalnumber="2149" number="290" form="verse">If it appear not plain and prove untrue,</line>
<line globalnumber="2150" number="291" form="verse">Deadly divorce step between me and you!</line>
<line globalnumber="2151" number="292" form="verse">O my dear mother, do I see you living?</line>
</speech>

<speech>
<speaker long="Lafew">LAF.</speaker>
<line globalnumber="2152" number="293" form="verse">Mine eyes smell onions, I shall weep anon.</line>
<stagedir sdglobalnumber="2152.01" sdnumber="293.01">
	<dir>To Parolles.</dir>
	<action type="speak">
		<actor>LAF.</actor>
		<recipient>PAR.</recipient>
	</action>
</stagedir>
<line globalnumber="2153" number="294" form="prose">Good Tom Drum, lend me a handkercher. So, I thank thee; wait on me home, I&#8217;ll make sport with thee. Let thy curtsies alone, they are scurvy ones.</line>
</speech>

<speech>
<speaker long="King of France">KING.</speaker>
<line globalnumber="2154" number="295" form="verse">Let us from point to point this story know,</line>
<line globalnumber="2155" number="296" form="verse">To make the even truth in pleasure flow.</line>
<stagedir sdglobalnumber="2155.01" sdnumber="296.01">
	<dir>To Diana.</dir>
	<action type="speak">
		<actor>KING.</actor>
		<recipient>DIA.</recipient>
	</action>
</stagedir>
<line globalnumber="2156" number="297" form="verse">If thou beest yet a fresh uncropped flower,</line>
<line globalnumber="2157" number="298" form="verse">Choose thou thy husband, and I&#8217;ll pay thy dower,</line>
<line globalnumber="2158" number="299" form="verse">For I can guess that by thy honest aid</line>
<line globalnumber="2159" number="300" form="verse">Thou kept&#8217;st a wife herself, thyself a maid.</line>
<line globalnumber="2160" number="301" form="verse">Of that and all the progress, more and less,</line>
<line globalnumber="2161" number="302" form="verse">Resolvedly more leisure shall express.</line>
<line globalnumber="2162" number="303" form="verse">All yet seems well, and if it end so meet,</line>
<line globalnumber="2163" number="304" form="verse">The bitter past, more welcome is the sweet.</line>
</speech>

<stagedir sdglobalnumber="2163.01" sdnumber="304.01">
	<dir>Flourish.</dir>
	<action type="exit">
		<actor>KING.</actor>
		<actor>COUNT.</actor>
		<actor>LAF.</actor>
		<actor>1. LORD. DUM.</actor>
		<actor>2. LORD. DUM.</actor>
		<actor>GENT.</actor>
		<actor>BER.</actor>
		<actor>DIA.</actor>
		<actor>PAR.</actor>
		<actor>WID.</actor>
		<actor>HEL.</actor>
		<actor>Attendants</actor>
	</action>
</stagedir>

</scene>

</act>

<epilogue>
<scenetitle type="epilogue">Epilogue</scenetitle>
<scenepersonae>
	<scenepersona short="KING.">King</scenepersona>
</scenepersonae>
<scenelanguage>
    <language short="en">English</language>
</scenelanguage>


<speech type="soliloquy">
<speaker long="King of France">KING.</speaker>

<stagedir sdglobalnumber="2163.02" sdnumber="0.01">
	<dir>Advancing.</dir>
	<action type="enter">
		<actor>KING.</actor>
	</action>
</stagedir>
<line globalnumber="2164" number="1" form="verse">The king&#8217;s a beggar, now the play is done;</line>
<line globalnumber="2165" number="2" form="verse">All is well ended, if this suit be won,</line>
<line globalnumber="2166" number="3" form="verse">That you express content; which we will pay,</line>
<line globalnumber="2167" number="4" form="verse">With strife to please you, day exceeding day.</line>
<line globalnumber="2168" number="5" form="verse">Ours be your patience then, and yours our parts;</line>
<line globalnumber="2169" number="6" form="verse">Your gentle hands lend us, and take our hearts.</line>
</speech>

<stagedir sdglobalnumber="2169.01" sdnumber="6.01">
	<dir>Exeunt omnes.</dir>
	<action type="exit">
		<actor>KING.</actor>
	</action>
</stagedir>
</epilogue>






<sources>

<playsource>
<playsourcetitle>The Palace of Pleasure</playsourcetitle>
<playsourceauthor>William Painter</playsourceauthor>
<playsourcedate>1575</playsourcedate>
</playsource>

<textsources>
<textsource title="Folio" edition="1" date="1623">First Folio</textsource>
</textsources>

</sources>

<sourcedetails>
<source>PlayShakespeare.com</source>
<sourceurl>http://www.playshakespeare.com</sourceurl>
<copyright>2005-2019 by PlayShakespeare.com</copyright>
<version>4.1</version>
<license>GFDL License 1.3</license>
<licenseurl>http://www.gnu.org/copyleft/fdl.html</licenseurl>
<termsurl>http://www.playshakespeare.com/license</termsurl>
</sourcedetails>

</play>"""
    print(extract_xml(text))
