<?php
// src/Command/CreateUserCommand.php
namespace App;

use Generator;
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Helper\ProgressBar;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\DomCrawler\Crawler;
use Symfony\Component\HttpClient\HttpClient;

// the name of the command is what users type after "php bin/console"
#[AsCommand(name: 'app:get-best-theme-team')]
class GetBestThemeTeam extends Command
{
  private const ALL_TEAMS = [
    'arizona-cardinals',
    'atlanta-falcons',
    'baltimore-ravens',
    'buffalo-bills',
    'carolina-panthers',
    'chicago-bears',
    'cincinnati-bengals',
    'cleveland-browns',
    'dallas-cowboys',
    'denver-broncos',
    'detroit-lions',
    'green-bay-packers',
    'houston-texans',
    'indianapolis-colts',
    'jacksonville-jaguars',
    'kansas-city-chiefs',
    'las-vegas-raiders',
    'los-angeles-chargers',
    'los-angeles-rams',
    'miami-dolphins',
    'minnesota-vikings',
    'new-england-patriots',
    'new-orleans-saints',
    'new-york-giants',
    'new-york-jets',
    'philadelphia-eagles',
    'pittsburgh-steelers',
    'san-francisco-49ers',
    'seattle-seahawks',
    'tampa-bay-buccaneers',
    'tennessee-titans',
    'washington-commanders',
  ];

  protected function execute(InputInterface $input, OutputInterface $output): int
  {
    $progressBar = new ProgressBar($output);
    $progressBar->setFormat(' %current%/%max% [%bar%] %percent:3s%% %elapsed:16s%/%estimated:-16s% %memory:6s% %message%');
    $progressBar->setMessage('Starting...');
    $result = [];
    $client = HttpClient::create();
    $baseUrl = 'https://www.mut.gg/theme-teams/hybrid';
    $fp = fopen(__DIR__ . '/../files/result.csv', 'w');
    fputcsv($fp, ["Team 1", "Team 2", "Team 3", "Overall"]);
    foreach ($progressBar->iterate($this->getAllCombinationOfThree()) as $combo) {
      $implodedCombo = implode(',', $combo);
      $query = http_build_query(['teams' => $implodedCombo]);
      $response = $client->request(
        'GET',
        "{$baseUrl}?{$query}"
      );
      $crawler = new Crawler($response->getContent());
      $ratingContent = $crawler
        ->filterXPath('//h3[contains(text(), "Overall Ratings")]')
        ->nextAll()
        ->text();
      $ratingContent = preg_replace('/^.*?(\d+\.\d+).*$/', '$1', $ratingContent);
      $progressBar->setMessage("{$implodedCombo}: {$ratingContent}");
      $result[$implodedCombo] = $ratingContent;
      $csv = [];
      foreach ($combo as $team) {
        $csv[] = implode(
          ' ',
          array_map('ucfirst', explode('-', $team))
        );
      }
      $csv[] = (string) $ratingContent;
      fputcsv($fp, $csv);
    }

    fclose($fp);
    asort($result);
    $bestCombo = array_key_last($result);
    $bestResult = $result[$bestCombo];
    $output->writeln("{$bestCombo}: {$bestResult}");
    return self::SUCCESS;
  }

  private function getAllCombinationOfThree(): array
  {
    $return = [];
    $allTeamLength = count(self::ALL_TEAMS);
    for ($i = 0; $i < $allTeamLength; $i++) {
      for ($ii = $i + 1; $ii < $allTeamLength; $ii++) {
        for ($iii = $ii + 1; $iii < $allTeamLength; $iii++) {
          $return[] = [self::ALL_TEAMS[$i], self::ALL_TEAMS[$ii], self::ALL_TEAMS[$iii]];
        }
      }
    }
    return $return;
  }
}
