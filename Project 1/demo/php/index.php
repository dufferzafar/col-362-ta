<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>COL 362/632 - Project 1 - Demo PHP App</title>

    <style>
        /* 
            CSS style copied from https://divtable.com/table-styler/

            Minimalist Black Theme
         */
        table {
            border: 3px solid #000000;
            max-width: 800px;
            border-collapse: collapse;
        }

        table td,
        table th {
            border: 1px solid #000000;
            padding: 5px 4px;
        }

        table tbody td {
            font-size: 13px;
        }

        table thead {
            background: #CFCFCF;
            background: -moz-linear-gradient(top, #dbdbdb 0%, #d3d3d3 66%, #CFCFCF 100%);
            background: -webkit-linear-gradient(top, #dbdbdb 0%, #d3d3d3 66%, #CFCFCF 100%);
            background: linear-gradient(to bottom, #dbdbdb 0%, #d3d3d3 66%, #CFCFCF 100%);
            border-bottom: 3px solid #000000;
        }

        table thead th {
            font-size: 15px;
            font-weight: bold;
            color: #000000;
            text-align: left;
        }

        table tfoot {
            font-size: 14px;
            font-weight: bold;
            color: #000000;
            border-top: 3px solid #000000;
        }

        table tfoot td {
            font-size: 14px;
        }
    </style>

</head>

<body>

    <h1>PHP + PostgresSQL</h2>
    <p>This is a demo application created using plain PHP (with some CSS sprinkled in).</p>

    <h2 class="mt-5 ">Playstore Reviews Sentiment Analysis</h1>
    <p class="lead">Showing the results of: SELECT * FROM playstore ORDER BY random() LIMIT 25</p>

    <?php
    pg_connect("host=10.17.50.247 dbname=group_0 user=group_0 password='This is a long passphrase that no one can guess.'");
    $query = "SELECT * FROM playstore ORDER BY random() LIMIT 25";
    $rows = pg_query($query);
    ?>

    <table>
        <thead>
            <tr>
                <th>App Name</th>
                <th>Review</th>
                <th>Sentiment</th>
                <th>Polarity</th>
                <th>Subjectivity</th>
            </tr>
        </thead>

        <tbody>
            <?php while ($row = pg_fetch_array($rows)) {?>
            <tr>
                <td> <?php echo $row['app_name']; ?> </td>
                <td> <?php echo $row['review']; ?> </td>
                <td> <?php echo $row['senti']; ?> </td>
                <td> <?php echo $row['polarity']; ?> </td>
                <td> <?php echo $row['subjectivity']; ?> </td>
            </tr>
            <?php }?>
        </tbody>

    </table>


    <footer style="margin-top: 50px;">
    <hr>
        <span>
            Built by
            <a href="https://github.com/dufferZafar" target="_blank">@dufferZafar</a> and
            <a href="https://github.com/hthuwal" target="_blank">@hthuwal</a>
            using
            <a href="http: //php.net/manual/en/intro-whatis.php" target="_blank">PHP</a> &
            <a href="https://code.visualstudio.com" target="_blank">VSCode</a>.
        </span>

</body>

</html>
