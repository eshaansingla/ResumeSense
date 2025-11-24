"""
Power Verb Suggestion System
Identifies weak verbs in resumes and suggests stronger action verbs.
"""
import re
from typing import Dict, List, Tuple


class PowerVerbSuggester:
    """Suggest power verbs to replace weak verbs in resumes"""
    
    # Dictionary mapping weak verbs to strong action verbs
    VERB_REPLACEMENTS = {
        'did': ['executed', 'implemented', 'accomplished', 'achieved'],
        'made': ['created', 'developed', 'built', 'produced', 'established'],
        'got': ['obtained', 'acquired', 'secured', 'attained'],
        'helped': ['assisted', 'supported', 'facilitated', 'enabled', 'contributed'],
        'worked': ['collaborated', 'operated', 'functioned', 'performed'],
        'used': ['utilized', 'leveraged', 'employed', 'applied'],
        'fixed': ['resolved', 'repaired', 'corrected', 'remediated'],
        'changed': ['transformed', 'modified', 'improved', 'enhanced'],
        'started': ['initiated', 'launched', 'established', 'founded'],
        'managed': ['oversaw', 'directed', 'orchestrated', 'coordinated'],
        'led': ['spearheaded', 'headed', 'guided', 'championed'],
        'improved': ['enhanced', 'optimized', 'refined', 'upgraded'],
        'increased': ['boosted', 'amplified', 'expanded', 'elevated'],
        'decreased': ['reduced', 'minimized', 'lowered', 'cut'],
        'created': ['designed', 'developed', 'built', 'engineered'],
        'wrote': ['authored', 'composed', 'drafted', 'penned'],
        'talked': ['communicated', 'presented', 'addressed', 'conveyed'],
        'showed': ['demonstrated', 'exhibited', 'illustrated', 'presented'],
        'found': ['identified', 'discovered', 'uncovered', 'located'],
        'gave': ['provided', 'delivered', 'supplied', 'furnished'],
        'took': ['assumed', 'undertook', 'handled', 'managed'],
        'went': ['traveled', 'attended', 'participated'],
        'saw': ['observed', 'monitored', 'tracked', 'analyzed'],
        'tried': ['attempted', 'endeavored', 'pursued', 'sought'],
        'kept': ['maintained', 'preserved', 'sustained', 'retained'],
        'put': ['placed', 'positioned', 'installed', 'deployed'],
        'set': ['established', 'configured', 'arranged', 'organized'],
        'ran': ['executed', 'operated', 'administered', 'managed'],
        'did': ['performed', 'executed', 'accomplished', 'achieved'],
        'looked': ['examined', 'reviewed', 'analyzed', 'inspected'],
        'asked': ['inquired', 'requested', 'solicited', 'consulted'],
        'told': ['informed', 'notified', 'advised', 'communicated'],
        'met': ['collaborated', 'coordinated', 'convened', 'engaged'],
        'left': ['departed', 'transitioned', 'moved'],
        'came': ['arrived', 'joined', 'entered'],
        'said': ['stated', 'expressed', 'articulated', 'communicated'],
        'thought': ['analyzed', 'evaluated', 'considered', 'assessed'],
        'knew': ['understood', 'comprehended', 'grasped', 'mastered'],
        'learned': ['mastered', 'acquired', 'gained expertise in'],
        'taught': ['trained', 'instructed', 'educated', 'mentored'],
        'built': ['constructed', 'developed', 'engineered', 'architected'],
        'sold': ['marketed', 'promoted', 'distributed', 'commercialized'],
        'bought': ['procured', 'purchased', 'acquired', 'sourced'],
        'sent': ['delivered', 'transmitted', 'dispatched', 'forwarded'],
        'received': ['obtained', 'acquired', 'attained', 'secured'],
        'opened': ['launched', 'initiated', 'established', 'introduced'],
        'closed': ['finalized', 'completed', 'concluded', 'wrapped up'],
        'moved': ['relocated', 'transferred', 'transitioned', 'shifted'],
        'stayed': ['maintained', 'preserved', 'sustained', 'retained'],
        'turned': ['transformed', 'converted', 'changed', 'modified'],
        'pulled': ['extracted', 'retrieved', 'obtained', 'acquired'],
        'pushed': ['promoted', 'advanced', 'propelled', 'drove'],
        'held': ['maintained', 'preserved', 'sustained', 'retained'],
        'brought': ['delivered', 'introduced', 'provided', 'supplied'],
        'called': ['contacted', 'reached out', 'communicated', 'connected'],
        'played': ['performed', 'executed', 'operated', 'functioned'],
        'read': ['reviewed', 'analyzed', 'examined', 'studied'],
        'heard': ['listened', 'attended', 'participated'],
        'felt': ['perceived', 'recognized', 'identified', 'detected'],
        'seemed': ['appeared', 'demonstrated', 'exhibited'],
        'became': ['transformed into', 'evolved into', 'developed into'],
        'began': ['initiated', 'commenced', 'launched', 'started'],
        'ended': ['concluded', 'finalized', 'completed', 'wrapped up'],
        'happened': ['occurred', 'transpired', 'took place'],
        'mattered': ['impacted', 'influenced', 'affected', 'contributed'],
        'wanted': ['sought', 'desired', 'aimed for', 'pursued'],
        'needed': ['required', 'demanded', 'necessitated'],
        'tried': ['attempted', 'endeavored', 'strived', 'pursued'],
        'used': ['utilized', 'leveraged', 'employed', 'applied'],
        'worked': ['collaborated', 'operated', 'functioned', 'performed'],
        'called': ['contacted', 'reached out', 'communicated', 'connected'],
        'asked': ['inquired', 'requested', 'solicited', 'consulted'],
        'tried': ['attempted', 'endeavored', 'pursued', 'sought'],
        'got': ['obtained', 'acquired', 'secured', 'attained'],
        'went': ['traveled', 'attended', 'participated'],
        'saw': ['observed', 'monitored', 'tracked', 'analyzed'],
        'came': ['arrived', 'joined', 'entered'],
        'knew': ['understood', 'comprehended', 'grasped', 'mastered'],
        'thought': ['analyzed', 'evaluated', 'considered', 'assessed'],
        'took': ['assumed', 'undertook', 'handled', 'managed'],
        'gave': ['provided', 'delivered', 'supplied', 'furnished'],
        'told': ['informed', 'notified', 'advised', 'communicated'],
        'said': ['stated', 'expressed', 'articulated', 'communicated'],
        'went': ['traveled', 'attended', 'participated'],
        'saw': ['observed', 'monitored', 'tracked', 'analyzed'],
        'came': ['arrived', 'joined', 'entered'],
        'knew': ['understood', 'comprehended', 'grasped', 'mastered'],
        'thought': ['analyzed', 'evaluated', 'considered', 'assessed'],
        'took': ['assumed', 'undertook', 'handled', 'managed'],
        'gave': ['provided', 'delivered', 'supplied', 'furnished'],
        'told': ['informed', 'notified', 'advised', 'communicated'],
        'said': ['stated', 'expressed', 'articulated', 'communicated']
    }
    
    @staticmethod
    def find_weak_verbs(resume_text: str) -> List[Dict]:
        """
        Find weak verbs in resume text and suggest replacements.
        
        Args:
            resume_text: Resume text to analyze
            
        Returns:
            List of dictionaries with weak verb findings and suggestions
        """
        findings = []
        text_lower = resume_text.lower()
        
        # Find all verb instances
        for weak_verb, strong_verbs in PowerVerbSuggester.VERB_REPLACEMENTS.items():
            # Create pattern to find the verb (word boundary to avoid partial matches)
            pattern = r'\b' + re.escape(weak_verb) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            
            if matches:
                for match in matches:
                    # Get context around the verb (20 chars before and after)
                    start = max(0, match.start() - 20)
                    end = min(len(resume_text), match.end() + 20)
                    context = resume_text[start:end]
                    
                    findings.append({
                        'weak_verb': weak_verb,
                        'suggestions': strong_verbs[:3],  # Top 3 suggestions
                        'context': context.strip(),
                        'position': match.start()
                    })
        
        # Sort by position in text
        findings.sort(key=lambda x: x['position'])
        
        # Remove duplicates (same verb in same context area)
        unique_findings = []
        seen_contexts = set()
        for finding in findings:
            context_key = (finding['weak_verb'], finding['context'][:30])
            if context_key not in seen_contexts:
                seen_contexts.add(context_key)
                unique_findings.append(finding)
        
        return unique_findings[:20]  # Limit to top 20 findings
    
    @staticmethod
    def get_power_verb_stats(resume_text: str) -> Dict:
        """
        Get statistics about power verbs in the resume.
        
        Args:
            resume_text: Resume text to analyze
            
        Returns:
            Dictionary with power verb statistics
        """
        text_lower = resume_text.lower()
        
        # Count weak verbs found
        weak_verb_count = 0
        weak_verbs_found = []
        
        for weak_verb in PowerVerbSuggester.VERB_REPLACEMENTS.keys():
            pattern = r'\b' + re.escape(weak_verb) + r'\b'
            matches = len(re.findall(pattern, text_lower))
            if matches > 0:
                weak_verb_count += matches
                weak_verbs_found.append({
                    'verb': weak_verb,
                    'count': matches
                })
        
        # Count strong action verbs (common power verbs)
        strong_verbs = [
            'achieved', 'accomplished', 'executed', 'implemented', 'developed',
            'created', 'designed', 'built', 'established', 'launched',
            'managed', 'led', 'directed', 'oversaw', 'coordinated',
            'improved', 'enhanced', 'optimized', 'increased', 'boosted',
            'reduced', 'minimized', 'resolved', 'solved', 'delivered',
            'produced', 'generated', 'secured', 'obtained', 'acquired'
        ]
        
        strong_verb_count = 0
        for verb in strong_verbs:
            pattern = r'\b' + re.escape(verb) + r'\b'
            strong_verb_count += len(re.findall(pattern, text_lower))
        
        return {
            'weak_verb_count': weak_verb_count,
            'strong_verb_count': strong_verb_count,
            'weak_verbs_found': sorted(weak_verbs_found, key=lambda x: x['count'], reverse=True)[:10],
            'power_verb_score': round(
                (strong_verb_count / max(weak_verb_count + strong_verb_count, 1)) * 100, 2
            )
        }


