"""Static CI coverage checks; browser execution stays in the platform workflow."""
from pathlib import Path
import ast,re,unittest
ROOT=Path(__file__).resolve().parents[1]
class BrowserTaskCoverage(unittest.TestCase):
 def test_every_workflow_browser_entry_point_and_helper_parses(self):
  workflow=(ROOT/'.github/workflows/pt-m1-qa.yml').read_text('utf-8')
  paths=set(re.findall(r'python (tests/browser_[\w]+\.py)',workflow))
  # A dedicated matrix job may add its own driver; never reduce the core CI inventory.
  self.assertGreaterEqual(len(paths),29)
  self.assertTrue({'tests/browser_unit_routes.py','tests/browser_unit_synthesis.py',
                   'tests/browser_unit_support.py','tests/browser_ux06_pt.py',
                   'tests/browser_m1_and_inventory.py'}.issubset(paths))
  for path in sorted(paths|{'tests/browser_task_contract.py','tests/browser_task_lesson_matrix.py'}):
   ast.parse((ROOT/path).read_text('utf-8'),filename=path)
 def test_new_task_checks_are_called_from_existing_ci_entry_points(self):
  route=(ROOT/'tests/browser_unit_routes.py').read_text('utf-8')
  self.assertIn('assert_task_route(page, m, plan',route)
  self.assertIn('visit_task_from_route(page, m, 1, hrefs[0])',route)
  self.assertIn("captured['count'] == 8",route)
  helper=(ROOT/'tests/browser_task_contract.py').read_text('utf-8')
  for contract in ('learning_storage(page) == before','button.press(\'Enter\')',
                   "feedback.inner_text() == button.get_attribute('data-response')",
                   'data-cartaz','route-teacher-tools'):
   self.assertIn(contract,helper)
 def test_responsive_matrix_is_invoked_and_checks_the_actual_viewport(self):
  helper=(ROOT/'tests/browser_task_contract.py').read_text('utf-8')
  driver=(ROOT/'tests/browser_task_lesson_matrix.py').read_text('utf-8')
  route=(ROOT/'tests/browser_unit_routes.py').read_text('utf-8')
  self.assertIn('responsive_task_matrix(browser,',driver)
  self.assertNotIn('responsive_task_matrix(browser, host)',route)
  for contract in ('for width in (390, 1366)',"for scheme in ('light', 'dark')",
                   "page.evaluate('innerWidth') == width",'assert_task_page(page, before)',
                   "anchor.press('Enter')",'launcher.click()',
                   "page.frame_locator('#lesson-frame')"):
   self.assertIn(contract,helper)
 def test_inventory_and_lesson_feedback_coverage_stays_enabled(self):
  source=(ROOT/'tests/browser_m1_and_inventory.py').read_text('utf-8')
  for original in ('assert len(pages) == 109','for width in (320, 1440)',
                   "saved['lida'] and saved['tentativas'] >= 1",
                   "assert len(text) > 60"):
   self.assertIn(original,source)
if __name__=='__main__':unittest.main()
